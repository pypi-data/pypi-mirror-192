# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databricks_access_layer', 'databricks_access_layer.aws']

package_data = \
{'': ['*']}

install_requires = \
['absl-py>=1.4.0,<2.0.0',
 'cachetools>=5.3.0,<6.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyspark>=3.3.1,<4.0.0',
 'quinn>=0.9.0,<0.10.0',
 'snowflake-connector-python>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'databricks-access-layer',
    'version': '0.0.1',
    'description': 'Library to access Snowflake data from Databricks',
    'long_description': 'None',
    'author': 'Data',
    'author_email': 'data@superside.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.1,<3.11',
}


setup(**setup_kwargs)
