# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlflow_token']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['mlflow-token = mlflow_token.mlflow-token:run']}

setup_kwargs = {
    'name': 'mlflow-token',
    'version': '0.1.1',
    'description': 'Command line tool to retreive access token for mlflow instance',
    'long_description': "# mlflow-token\nObtain an access token for an MLFlow instance deployed behind OAuth2-proxy and\nkeycloak. \n\nThis script will use your current setting of `MLFLOW_TRACKING_URI` to look for\nthe keycloak redirect from it's OAuth2-proxy. From there it will start an\nOAuth device flow to allow you to obtain a valid access token. This token will\nbe set in your environment's `MLFLOW_TRACKING_TOKEN` variable for use by the\nMLFlow client libraries.\n\nYou can also specify the `--echo` command line argument to get the tool to print\na command for assigning the token to the environment variable.\n",
    'author': 'Ben Galewsky',
    'author_email': 'bengal1@illinois.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ncsa/mlflow-token',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
