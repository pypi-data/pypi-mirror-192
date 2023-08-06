from collections.abc import Mapping
import logging
import os
import re
from functools import partial

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from murmuration import kms_wrapped
from .bunch import Bunch
from .aws import yield_parameters
from .aws import get_parameter
from .aws import put_parameter
from .aws import delete_parameters
from .aws import ssm_key


__all__ = [
    'ParamBunch',
]


dict_class = CommentedMap


def ssm_scalar_constructor(loader, node, profile=None, region=None):
    key = loader.construct_scalar(node)
    return get_parameter(key, profile=profile, region=region)


class Yaml(YAML):
    def __init__(self, profile=None, region=None):
        super().__init__(typ='rt')
        self.explicit_start = True
        self.preserve_quotes = True
        self.indent(sequence=4, mapping=2, offset=2)
        if profile or region:
            fn = partial(
                ssm_scalar_constructor,
                profile=profile,
                region=region)
            self.constructor.add_constructor('!ssm', fn)


def dump_yaml(x, filename):
    y = Yaml()
    if isinstance(filename, str):
        with open(filename, 'w') as f:
            y.dump(x, f)
    else:
        y.dump(x, filename)


class ParamBunch(Bunch):
    def __init__(self, values=None, prefix=None, filename=None):
        super().__init__(values)
        super()._set('original_values', values)
        super()._set('encrypted', [])
        super()._set('spinner', None)
        if prefix or filename:
            self.load(prefix=prefix, filename=filename)

    def _is_reserved(self, key):
        if key in [ 'values', 'original_value', 'encrypted', 'spinner', ]:
            return True
        return key in self.__dict__ and not key.startswith('__')

    def aws_items(self, values=None, prefix=None):
        prefix = prefix or [ '', self.meta.namespace ]
        for key, value in self.items(values, prefix):
            if '.meta.' in key:
                continue
            key = key.replace('.', '/')
            yield key, value

    def file_items(self, values=None, prefix=None):
        meta_prefix = re.compile(r'^\.?meta\.')
        for key, value in self.items(values, prefix):
            if meta_prefix.match(key):
                continue
            yield key, value
        yield from self.items(values=self.meta.values, prefix=[ 'meta' ])

    def to_dict(self):
        result = super().to_dict()
        return result

    @staticmethod
    def _traverse(d, prefix=None):
        prefix = prefix or []
        for key, value in d.items():
            if isinstance(value, Mapping):
                yield from ParamBunch._traverse(value, prefix + [ key ])
            else:
                yield '.'.join(prefix + [ key ]), value

    @staticmethod
    def try_decrypt(value, region=None, profile=None, session=None):
        if isinstance(value, str):
            try:
                value = kms_wrapped.decrypt(value, region, profile, session)
            except ValueError:
                pass
        return value

    def from_file(self, filename, decrypt=True, handle_tags=True):
        # late load logger in case anyone sets up logging
        # later
        log = logging.getLogger(__name__)
        if not os.path.exists(filename):
            log.warning('waddle: could not find %s', filename)
            return

        with open(filename, 'r', encoding='utf-8') as f:
            y = Yaml()
            data = y.load(f)
            # double parse the file so that we can pick up
            # the meta values before trying to construct
            # any custom !ssm tags
            meta = data.get('meta', {})
            region = meta.get('region')
            profile = meta.get('profile')
        if handle_tags:
            with open(filename, 'r', encoding='utf-8') as f:
                y = Yaml(profile=profile, region=region)
                data = y.load(f)
        super()._set('original_values', data)
        values = []
        for key, value in ParamBunch._traverse(data):
            if self._is_reserved(key):
                raise KeyError(f'`{key}` is not a valid key name')
            if key.startswith('meta.'):
                self[key] = value
            else:
                values.append((key, value))
        self.handle_file_values(values, decrypt)

    def handle_file_values(self, values, decrypt):
        region = self.get('meta.region')
        profile = self.get('meta.profile')
        for key, value in values:
            if not decrypt:
                self[key] = value
                continue
            self[key] = ParamBunch.try_decrypt(value, region, profile)
            if self[key] != value:
                self.encrypted.append(key)

    def load(self, prefix=None, filename=None, decrypt=True):
        if prefix:
            self.from_aws(prefix)
        if filename:
            self.from_file(filename, decrypt)

    def from_aws(self, prefix):
        if not prefix.startswith('/'):
            prefix = f'/{prefix}'
        prefix = prefix.replace('.', '/')
        for key, value, type_ in yield_parameters(prefix):
            if type_ == 'SecureString':
                self.encrypted.append(key)
            elif type_ == 'StringList':
                value = value.split(',')
            self[key] = value
        self.meta.namespace = prefix[1:].replace('/', '.')

    def _encrypted_keys(self):
        namespace = self.get('meta.namespace', '')
        ms_encrypted = set()
        for x in self.encrypted:
            ms_encrypted.add(ssm_key(namespace, x))
        return ms_encrypted

    def to_aws(self, force_encryption=False, verbose=True):
        ms_encrypted = self._encrypted_keys()
        kms_key = self.get('meta.kms_key')
        for key, value in self.aws_items():
            encrypted = key in ms_encrypted
            encrypted = encrypted or force_encryption
            put_parameter(key, value, kms_key, encrypted, verbose)

    def delete_from_aws(self, verbose=True):
        keys = [ key for key, _ in self.aws_items() ]
        delete_parameters(*keys, verbose=verbose)

    def original_value(self, key):
        data = self.original_values
        if key in data:
            return data, key, data[key]
        pieces = key.split('.')
        for x in pieces[:-1]:
            data = data[x]
        key = pieces[-1]
        return data, key, data[key]

    def original_parent(self, key):
        data = self.original_values
        pieces = key.split('.')
        try:
            for x in pieces[:-1]:
                data = data[x]
            return data, pieces[-1]
        except (KeyError, TypeError):
            return self.original_values, key

    def fill_back(self):
        updated_values = []
        new_values = []
        for key, value in self.items():
            try:
                parent, key, original_value = self.original_value(key)
                if value != original_value:
                    updated_values.append((parent, key, value))
            except (KeyError, TypeError):
                new_values.append((key, value))
        self.handle_updates(updated_values)
        self.handle_new(new_values)

    def handle_updates(self, updated_values):
        # pylint: disable=access-member-before-definition
        for parent, key, value in updated_values:
            parent[key] = value
        if self.original_values is None:
            self.original_values = dict_class()

    def handle_new(self, new_values):
        for key, value in new_values:
            parent, x = self.original_parent(key)
            parent[x] = value

    def save(self, filename):
        self.fill_back()
        dump_yaml(self.original_values, filename)
