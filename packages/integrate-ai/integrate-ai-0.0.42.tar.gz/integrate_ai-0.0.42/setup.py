# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['integrate_ai', 'integrate_ai.utils']

package_data = \
{'': ['*']}

install_requires = \
['docker>=6.0.1,<7.0.0', 'pyjwt==2.6.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['iai = integrate_ai.cli:main']}

setup_kwargs = {
    'name': 'integrate-ai',
    'version': '0.0.42',
    'description': 'integrate.ai Command Line Interface',
    'long_description': "# integrate.ai Command Line Interface\n\nA CLI that enables users to interact with integrate.ai's software.\n\nThis tool allows users to manage client and sdk packages. Use the integate.ai sdk to seamlessly integrate federated learning and analytics workflows directly into your product.\n\n## Installation\n\nintegrate-ai requires `Python >= 3.8`\n\n```\npip install integrate-ai\n```\n\n## Quick Start\n\nCreate a new IAI token through the integrate.ai UI.\n\n### Install integrate-ai-sdk\n\n```\niai sdk install --token <IAI_TOKEN> \n```\n\n### Pull integrate.ai docker client\n\n```\niai client pull --token <IAI_TOKEN> \n```\n\n### Run integrate.ai training session\n\n```\niai client train --token <IAI_TOKEN> --session <SESSION_ID> --train_path <PATH_TO_TRAINING_DATA> --test_path <PATH_TO_TEST_DATA> --batch_size 5\n```\n",
    'author': 'integrate.ai',
    'author_email': 'contact@integrate.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://integrate.ai',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
