"""A utility for Python's dict.


Example
-------

    >>> import umuus_dict_util

    >>> umuus_dict_util.to_dict('a.b.c', 1)
    {'a': {'b': {'c': 1}}}

    >>> umuus_dict_util.from_paths({"a.b": 1, "a.c": 1})
    {'a': {'c': 1, 'b': 1}}

    >>> umuus_dict_util.to_paths({'a': {'c': 1, 'b': 1}})
    {'a.c': 1, 'a.b': 1}

    >>> umuus_dict_util.get('a.b.c', {"a": {"b": {"c": 1}}})
    1

    >>> umuus_dict_util.merge({"x": {"y": 1}}, {"x": {"z": 1}})
    {'x': {'z': 1, 'y': 1}}

    >>> umuus_dict_util.merge_all([{"x": {"y": 1}}, {"x": {"z": 1}}, {"a": {"b": 1}}])
    {'a': {'b': 1}, 'x': {'z': 1, 'y': 1}}

    >>> umuus_dict_util.merge({'a': {'b': 1}}, {'a': {'c': 1}}, replace=False)
    {'a': {'c': 1, 'b': 1}}

    >>> umuus_dict_util.merge_all([{'a': {'b': 1}}, {'a': {'b': 2}}, {'a': {'b': 3}}], replace=False)
    {'a': {'b': [1, 2, 3]}}

   >>> umuus_dict_util.parse_args(['-a.b.c', '1', '-a.b.d', '1'])
   {'a': {'b': {'c': 1, 'd': 1}}}

"""
import re
import sys
import json
import jmespath
__version__ = '0.1'
__url__ = 'https://github.com/junmakii/umuus_dict_util'
__author__ = 'Jun Makii'
__author_email__ = 'junmakii@gmail.com'
__keywords__ = []
__license__ = 'GPLv3'
__scripts__ = []
__install_requires__ = [
    'jmespath',
]
__classifiers__ = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Programming Language :: Python',
    # 'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
]
__entry_points__ = {'console_scripts': []}
try:
    unicode
except NameError:
    unicode = str


def parse_args(args=[]):
    options = {}
    for key, value in zip(args[0:None:2], args[1:None:2]):
        key = re.sub('^-+', '', key)
        value = encode_json_value(value)
        if key in options:
            if isinstance(options[key], list):
                options[key] += [value]
            else:
                options[key] = [options[key], value]
        else:
            options[key] = value
    return from_paths(options)


def get(path, data, default=None):
    return (jmespath.search(path, data) or default)


def encode_json_value(s):
    try:
        return json.loads(s)
    except (TypeError, json.JSONDecodeError):
        return s

def to_dict(a, value, o=None, delimiter='.'):
    o = ({} if o is None else o)
    a = (a if isinstance(a, list) else a.split(delimiter))
    for i in range(len(a)):
        rest = a[i + 1:]
        if len(rest):
            o[a[i]] = {}
            to_dict(rest, value, o[a[i]])
            return o
        else:
            o[a[i]] = value
            return o


def merge(source, destination, replace=True):
    for key, value in source.items():
        if isinstance(value, dict):
            destination[key] = destination.get(key, {})
            merge(value, destination[key], replace=replace)
        else:
            if key in destination and not replace:
                if isinstance(destination[key], (list, tuple)):
                    destination[key] += [value]
                else:
                    destination[key] = [destination[key], value]
            else:
                destination[key] = value
    return destination


def merge_all(items, *args, **kwargs):
    new_items = {}
    for item in items:
        new_items = merge(item, new_items, *args, **kwargs)
    return new_items


def from_paths(paths, *args, **kwargs):
    new_paths = []
    for path, value in paths.items():
        new_paths.append(to_dict(path, value))
    return merge_all(new_paths, *args, **kwargs)


def to_json_safe(o):
    if isinstance(o, (list, tuple)):
        return [to_json_safe(i) for i in o]
    elif isinstance(o, dict):
        new_obj = {}
        for key, value in o.items():
            new_obj[key] = to_json_safe(value)
        return new_obj
    elif isinstance(o, (float, int, str)):
        return o
    else:
        return str(o)
    return o


def encode_to_strings(
        d,  # type: str
        encoding='utf-8'
):  # type: Any
    """
    Example::

        encode_to_strings(
        ... {u"a": u"a_1", u"b": [u"b_1", "b_2"],
        ... u"c": {u"d": u"d_1", "e": [u"e_1", u"e_2"]}})
        {'a': 'a_1', 'c': {'e': ['e_1', 'e_2'], 'd': 'd_1'}, 'b': ['b_1', 'b_2']}
    """
    if isinstance(d, unicode):
        return d.encode(encoding)
    elif isinstance(d, (tuple, list)):
        return type(d)((encode_to_strings(i) for i in d))
    elif isinstance(d, dict):
        new_d = {}
        for k, v in d.items():
            new_d[(k.encode(encoding) if isinstance(k, unicode) else k)
                  ] = encode_to_strings(v)
        return new_d
    else:
        return d


def decode_to_strings(d, encoding='utf-8'):
    """
    Example::

        decode_to_strings(
        ... {"a": "a_1", "b": ["b_1", "b_2"],
        ... u"c": {"d": "d_1", "e": ["e_1", "e_2"]}})
        {'a': 'a_1', u'c': {'e': ['e_1', 'e_2'], 'd': 'd_1'}, 'b': ['b_1', 'b_2']}

    """
    if isinstance(d, str):
        return d.decode(encoding)
    elif isinstance(d, (tuple, list)):
        return type(d)((encode_to_strings(i) for i in d))
    elif isinstance(d, dict):
        new_d = {}
        for k, v in d.items():
            new_d[
                (k if isinstance(k, str) else k)
            ] = encode_to_strings(v)
        return new_d
    else:
        return d


def to_paths(data={}, new_data={}, prefix='', delimiter='.'):
    for key, value in data.items():
        if isinstance(value, dict):
            to_paths(value,
                 prefix=delimiter.join([prefix, key] if prefix else [key]),
                 new_data=new_data,
                 delimiter=delimiter)
        else:
            new_data[delimiter.join([prefix, key])] = value
    return new_data
