# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['restore',
 'restore.management',
 'restore.management.commands',
 'restore.migrations']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-restic-backup',
    'version': '0.2.0',
    'description': 'Restore files or/and database backup from an environment (backup server) with encrypted secret file after decrypting it (secret file is defined in settings.BACKUP_CONF_FILE',
    'long_description': 'None',
    'author': 'Dedomainia',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
