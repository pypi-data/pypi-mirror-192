# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ftrack_sftp_accessor']

package_data = \
{'': ['*']}

install_requires = \
['ftrack-action-handler>=0.3.0,<0.4.0',
 'ftrack-python-api>=2.3.3,<3.0.0',
 'paramiko>=2.11.0,<3.0.0']

setup_kwargs = {
    'name': 'ftrack-sftp-accessor',
    'version': '0.5.0',
    'description': 'A ftrack sftp accessor',
    'long_description': 'None',
    'author': 'Ian Wootten',
    'author_email': 'hi@niftydigits.com',
    'maintainer': 'ftrack support',
    'maintainer_email': 'support@ftrack.com',
    'url': 'https://github.com/ftrackhq/ftrack-sftp-accessor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.9,<3.10',
}


setup(**setup_kwargs)
