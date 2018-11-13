

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