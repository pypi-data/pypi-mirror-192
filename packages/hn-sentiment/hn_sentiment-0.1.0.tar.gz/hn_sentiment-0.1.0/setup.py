# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hn_sentiment']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=9.4.0,<10.0.0',
 'py-executable-checklist==1.4.0',
 'pygifsicle>=1.0.7,<2.0.0',
 'pytest>=7.2.0,<8.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'rich>=13.0.0,<14.0.0',
 'vadersentiment>=3.3.2,<4.0.0']

entry_points = \
{'console_scripts': ['hn-sentiment = hn_sentiment.app:main']}

setup_kwargs = {
    'name': 'hn-sentiment',
    'version': '0.1.0',
    'description': 'Use VaderSentiment to analyze the sentiment of a post on HackerNews.',
    'long_description': '# HackerNews Sentiment Analysis\n\n[![PyPI](https://img.shields.io/pypi/v/hn-sentiment?style=flat-square)](https://pypi.python.org/pypi/hn-sentiment/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hn-sentiment?style=flat-square)](https://pypi.python.org/pypi/hn-sentiment/)\n[![PyPI - License](https://img.shields.io/pypi/l/hn-sentiment?style=flat-square)](https://pypi.python.org/pypi/hn-sentiment/)\n\nUse VaderSentiment to analyze the sentiment of a post on HackerNews.\n\n---\n\n**Documentation**: [https://namuan.github.io/hn-sentiment](https://namuan.github.io/hn-sentiment)\n\n**Source Code**: [https://github.com/namuan/hn-sentiment](https://github.com/namuan/hn-sentiment)\n\n**PyPI**: [https://pypi.org/project/hn-sentiment/](https://pypi.org/project/hn-sentiment/)\n\n---\n\n## Pre-requisites\n\n\n\n## Installation\n\n```sh\npip install hn-sentiment\n```\n\n## Acknowledgements\n\n- [VaderSentiment](https://example.org)\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * Python 3.7+\n  * [Poetry](https://python-poetry.org/)\n\n* Create a virtual environment and install the dependencies\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n```sh\npoetry shell\n```\n\n### Validating build\n```sh\nmake build\n```\n\n### Release process\nA release is automatically published when a new version is bumped using `make bump`.\nSee `.github/workflows/build.yml` for more details.\nOnce the release is published, `.github/workflows/publish.yml` will automatically publish it to PyPI.\n\n### Disclaimer\n\nThis project is not affiliated with PlantUML.\n',
    'author': 'namuan',
    'author_email': 'github@deskriders.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://namuan.github.io/hn-sentiment',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<4.0',
}


setup(**setup_kwargs)
