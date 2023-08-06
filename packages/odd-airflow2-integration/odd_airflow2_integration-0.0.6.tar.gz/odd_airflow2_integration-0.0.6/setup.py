# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odd_airflow2_integration', 'odd_airflow2_integration.dir']

package_data = \
{'': ['*']}

install_requires = \
['odd-models>=2.0.12,<3.0.0']

entry_points = \
{'airflow.plugins': ['OddPlugin = odd_airflow2_integration.plugin:OddPlugin']}

setup_kwargs = {
    'name': 'odd-airflow2-integration',
    'version': '0.0.6',
    'description': 'ODD integration with Airflow',
    'long_description': 'Odd Airflow 2 integration via listeners',
    'author': 'Open Data Discovery',
    'author_email': 'pypi@opendatadiscovery.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/opendatadiscovery/odd-airflow-2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
