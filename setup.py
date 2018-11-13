
from setuptools import setup, find_packages

setup(
    name='umuus_dict_util',
    description="A utility for Python's dict.",
    long_description=("A utility for Python's dict.\n"
 '\n'
 '\n'
 'Example\n'
 '-------\n'
 '\n'
 '    >>> import umuus_dict_util\n'
 '\n'
 "    >>> umuus_dict_util.to_dict('a.b.c', 1)\n"
 "    {'a': {'b': {'c': 1}}}\n"
 '\n'
 '    >>> umuus_dict_util.from_paths({"a.b": 1, "a.c": 1})\n'
 "    {'a': {'c': 1, 'b': 1}}\n"
 '\n'
 "    >>> umuus_dict_util.to_paths({'a': {'c': 1, 'b': 1}})\n"
 "    {'a.c': 1, 'a.b': 1}\n"
 '\n'
 '    >>> umuus_dict_util.get(\'a.b.c\', {"a": {"b": {"c": 1}}})\n'
 '    1\n'
 '\n'
 '    >>> umuus_dict_util.merge({"x": {"y": 1}}, {"x": {"z": 1}})\n'
 "    {'x': {'z': 1, 'y': 1}}\n"
 '\n'
 '    >>> umuus_dict_util.merge_all([{"x": {"y": 1}}, {"x": {"z": 1}}, {"a": '
 '{"b": 1}}])\n'
 "    {'a': {'b': 1}, 'x': {'z': 1, 'y': 1}}\n"
 '\n'
 "    >>> umuus_dict_util.merge({'a': {'b': 1}}, {'a': {'c': 1}}, "
 'replace=False)\n'
 "    {'a': {'c': 1, 'b': 1}}\n"
 '\n'
 "    >>> umuus_dict_util.merge_all([{'a': {'b': 1}}, {'a': {'b': 2}}, {'a': "
 "{'b': 3}}], replace=False)\n"
 "    {'a': {'b': [1, 2, 3]}}\n"
 '\n'
 "   >>> umuus_dict_util.parse_args(['-a.b.c', '1', '-a.b.d', '1'])\n"
 "   {'a': {'b': {'c': 1, 'd': 1}}}"),
    py_modules=['umuus_dict_util'],
    version='0.1',
    url='https://github.com/junmakii/umuus_dict_util',
    author='Jun Makii',
    author_email='junmakii@gmail.com',
    keywords=[],
    license='GPLv3',
    scripts=[],
    install_requires=['jmespath>=0.9.3'],
    classifiers=['Intended Audience :: Developers', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', 'Natural Language :: English', 'Programming Language :: Python', 'Programming Language :: Python :: 3'],
    entry_points={'console_scripts': []}
)

