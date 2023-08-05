# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_memoizer']

package_data = \
{'': ['*']}

install_requires = \
['cachier>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'file-memoizer',
    'version': '0.1.1',
    'description': 'Store function results across executions using cache files',
    'long_description': "# File Memoizer\n\n[![license](https://img.shields.io/github/license/lordjabez/file-memoizer?color=blue&label=License)](https://opensource.org/licenses/MIT)\n[![PyPi:version](https://img.shields.io/pypi/v/file-memoizer?color=blue&label=PyPI)](https://pypi.org/project/file-memoizer/)\n[![Tests](https://github.com/lordjabez/file-memoizer/actions/workflows/test.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/test.yml)\n[![Linter](https://github.com/lordjabez/file-memoizer/actions/workflows/lint.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/lint.yml)\n[![Security](https://github.com/lordjabez/file-memoizer/actions/workflows/scan.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/scan.yml)\n[![Release](https://github.com/lordjabez/file-memoizer/actions/workflows/release.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/release.yml)\n\nThis Python package makes it easy to store function results across executions using cache files.\nUnderlying functionality is provided by [cachier](https://github.com/python-cachier/cachier), but\nthis package adds a few conveniences, such as being able to ignore parameters that won't serialize.\n\n\n## Installation\n\nInstallation is via `pip`:\n\n```bash\npip install file-memoizer\n```\n\n\n## Usage\n\nTo cache a function's value, annotate it by calling the `memoize`\nfunction as follows:\n\n```python3\nimport file_memoizer\n\n@file_memoizer.memoize()\ndef double(n):\n    return 2 * n\n```\n\nBy default the cached values remain valid for a day. This can be changed\nwith the `cache_ttl` parameter:\n\n```python3\nimport datetime\nimport file_memoizer\n\nseven_days = cache_ttl=datetime.timedelta(days=7)\n@file_memoizer.memoize(cache_ttl=seven_days)\ndef triple(n):\n    return 3 * n\n```\n\nCache files are stored in `$HOME/.file-memoizer`, with one file per\ncombination of input parameters. An alternate location can be specified\nwith the `cache_directory` parameter:\n\n```python3\nimport datetime\nimport file_memoizer\n\ncustom_path = '/path/to/store/files'\n@file_memoizer.memoize(cache_directory=custom_path)\ndef quadruple(n):\n    return 4 * n\n```\n\nNormally all function arguments must be hashable for it to be safely cached. However,\nthere are situations where it's okay to ignore them, such as an object method whose\nreturn value doesn't depend on the object's internal state. In these cases, set\n`unhashable_args='ignore'` as shown below:\n\nclass Arithmetic():\n\n    @staticmethod\n    @file_memoizer.memoize()\n    def quintuple(n):\n         return 5 * n\n    \n    @file_memoizer.memoize(unhashable_args='ignore')\n    def multiply(self, x, y):\n        return x * y\n```\n",
    'author': 'Judson Neer',
    'author_email': 'judson.neer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lordjabez/file-memoizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
