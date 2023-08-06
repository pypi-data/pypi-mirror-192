# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['galilei', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['fire==0.4.0']

extras_require = \
{'dev': ['tox>=3.24.5,<4.0.0',
         'virtualenv>=20.13.1,<21.0.0',
         'pip>=22.0.3,<23.0.0',
         'twine>=3.8.0,<4.0.0',
         'pre-commit>=2.17.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.2.3,<2.0.0',
         'mkdocs-include-markdown-plugin>=3.2.3,<4.0.0',
         'mkdocs-material>=8.1.11,<9.0.0',
         'mkdocstrings>=0.18.0,<0.19.0',
         'mkdocs-autorefs>=0.3.1,<0.4.0',
         'mike>=1.1.2,<2.0.0'],
 'test': ['black>=22.3.0,<23.0.0',
          'isort==5.10.1',
          'flake8==4.0.1',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest>=7.0.1,<8.0.0',
          'pytest-cov>=3.0.0,<4.0.0']}

entry_points = \
{'console_scripts': ['galilei = galilei.cli:main']}

setup_kwargs = {
    'name': 'galilei',
    'version': '0.1.5',
    'description': 'the galilei project.',
    'long_description': '# galilei\n\n<a href="https://pypi.python.org/pypi/galilei">\n    <img src="https://img.shields.io/pypi/v/galilei.svg"\n        alt = "Release Status">\n</a>\n<a href="https://github.com/guanyilun/galilei/actions">\n    <img src="https://github.com/guanyilun/galilei/actions/workflows/release.yml/badge.svg?branch=master" alt="CI Status">\n</a>\n<a href="https://github.com/guanyilun/galilei/actions">\n    <img src="https://github.com/guanyilun/galilei/actions/workflows/dev.yml/badge.svg?branch=master" alt="CI Status">\n</a>\n<a href="https://guanyilun.github.io/galilei/">\n    <img src="https://img.shields.io/website/https/guanyilun.github.io/galilei/index.html.svg?label=docs&down_message=unavailable&up_message=available" alt="Documentation Status">\n</a>\n<a href="https://codecov.io/gh/guanyilun/galilei" >\n <img src="https://codecov.io/gh/guanyilun/galilei/branch/master/graph/badge.svg?token=0C3DT4IWP5"/>\n</a>\n<a href="https://opensource.org/licenses/MPL-2.0">\n<img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">\n</a>\n\n\n`galilei` is a software package that makes emulating a function easier. The motivation of emulating a function is that sometimes computing a function could be a time consuming task, so one may need to find fast approximations of a function that\'s better than basic interpolation techniques. It builds on the ideas of\n[cosmopower](https://github.com/alessiospuriomancini/cosmopower) and [axionEmu](https://github.com/keirkwame/axionEmu), with an aim to be as generic and flexible as possible on the emulating target. As such, `galilei` can take any generic parametrized function that returns an array without a need to know its implementation detail.\n\n## Installation\n```\npip install galilei\n```\n\n## Basic usage\nSuppose that we have an expensive function that we want to emulate\n```python\ndef test(a=1, b=1):\n    x = np.linspace(0, 10, 100)\n    return np.sin(a*x) + np.sin(b*x)\n```\nIf you want to emulate this function, you can simply add a decorator `@emulate` and supply the parameters that you want to evaluate this function at to build up the training data set.\n\n```python\nfrom galilei import emulate\n\n@emulate(samples={\n    \'a\': np.random.rand(1000),\n    \'b\': np.random.rand(1000)\n})\ndef test(a=1, b=1):\n    x = np.linspace(0, 10, 100)\n    return np.sin(a*x) + np.sin(b*x)\n```\nHere we are just making 1000 pairs of random numbers from 0 to 1 to train our function. When executing these lines, the emulator will start training, and once it is done, the original `test` function will be automatically replaced with the emulated version and should behave in the same way, except much faster!\n```\nTraining emulator...\n100%|██████████| 500/500 [00:09<00:00, 50.50it/s, loss=0.023]\nAve Test loss: 0.025\n```\n![Comparison](https://github.com/guanyilun/galilei/raw/master/data/demo.png)\n\nFor more detailed usage examples, see this notebook:\n<a href="https://colab.research.google.com/drive/1_pvuAIqLUz4gV1vxytueb7AMR6Jmx-8n?usp=sharing">\n<img src="https://user-content.gitlab-static.net/dfbb2c197c959c47da3e225b71504edb540e21d6/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667" alt="open in colab">\n</a>\n## Features\n\n* TODO support saving trained model and load pretrained model\n* TODO add Gpy backend for gaussian process regression\n\n## Credits\nThis package was created with the [ppw](https://zillionare.github.io/python-project-wizard) tool. For more information, please visit the [project page](https://zillionare.github.io/python-project-wizard/).\n\nFree software: MIT\n',
    'author': 'Yilun Guan',
    'author_email': 'zoom.aaron@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/guanyilun/galilei',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
