# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyDeco',
 'pyDeco.cli',
 'pyDeco.debug',
 'pyDeco.debug.debug',
 'pyDeco.fun',
 'pyDeco.info']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'pytest>=7.2.1,<8.0.0']

setup_kwargs = {
    'name': 'python-deco',
    'version': '0.3.26',
    'description': '',
    'long_description': '<div align="center">\n\n<h1> <strong>py</strong>thon <strong>Deco</strong>ractor<br>\n<img src="https://img.shields.io/badge/made%20with-LOVE-red">\n<img src="https://img.shields.io/badge/license-MIT-blue">\n<a href=\'https://py-decorators.readthedocs.io/en/latest/?badge=latest\'>\n    <img src=\'https://readthedocs.org/projects/py-decorators/badge/?version=latest\' alt=\'Documentation Status\' />\n</a>\n</h1>\n</div>\n\nAn OSS that has something to do with decorators in python\n\n# :sparkles: Features\n\n- Time related decorators\n- Debugging decorators\n- Custom cli input decorators\n\n# :hammer: Install\n\nTo install, run the following command.\n\n```bash\n$ pip install python-deco\n```\n\n# :package: Modules\n\n- **Info**: Decorators that provide information about the function.\n\n- **Debug**: Decorators that help debug the function.\n\n- **CLI**: Decorators that uses variables defined in a [yaml/json] file as function arugments.\n\n- **Fun**: Decorators just for FUN!\n\n# :books: Usage\n\nA quick usage example.\n\n@timeit\n\n```python\nfrom pyDeco.dev import inactive\nfrom pyDeco.time import timeit\n\n@timeit\ndef func():\n    # do something\n    return 1\n```\n\n```bash\n2023-02-17 00:05:09,721 [INFO ] Function func() took 2.0120s.\n```\n\n# :construction: TODO\n\n## credits\n\nhttps://bytepawn.com/python-decorators-for-data-scientists.html\n',
    'author': 'adrian',
    'author_email': 'tamkayeung.adrian@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://py-decorators.readthedocs.io/en/latest/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
