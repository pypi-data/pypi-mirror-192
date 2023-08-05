# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['science_book',
 'science_book.physics',
 'science_book.physics.constants',
 'science_book.physics.mechanics',
 'science_book.units']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.10"': ['importlib-metadata>=5.0.0,<6.0.0']}

setup_kwargs = {
    'name': 'science-book',
    'version': '0.1.0a0.dev0',
    'description': 'A package to help everyday users with science calculations',
    'long_description': '# Science-Book\n\nAn open-source and freely available scientific library for scientists, students, educators, and enthusiasts.\n\n## Installation\n\n```bash\n$ pip install science-book\n```\n',
    'author': 'Gary Hammock',
    'author_email': 'ghammock79@gmail.com',
    'maintainer': 'Gary Hammock',
    'maintainer_email': 'ghammock79@gmail.com',
    'url': 'https://github.com/ghammock/science-book',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
