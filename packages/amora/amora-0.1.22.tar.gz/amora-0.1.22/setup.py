# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amora',
 'amora.cli',
 'amora.dash',
 'amora.dash.components',
 'amora.dash.components.filters',
 'amora.dash.gunicorn',
 'amora.dash.pages',
 'amora.feature_store',
 'amora.providers',
 'amora.tests']

package_data = \
{'': ['*'], 'amora': ['target/*', 'templates/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'SQLAlchemy[mypy]>=1.4,<2.0',
 'fsspec>=2022.5.0,<2023.0.0',
 'gcsfs>=2022.5.0,<2023.0.0',
 'humanize>=4.2.3,<5.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'networkx[all]>=2.6.3,<3.0.0',
 'pandas[output-formatting]>=1.3.0,<2.0.0',
 'protobuf>3,<5',
 'pydantic[email]>=1.10.2,<2.0.0',
 'pytest-xdist[psutil]>=2.5,<4.0',
 'pytest>=6.2.5,<8.0.0',
 'rich>=10.13,<13.0',
 'shed>=0.9.5,<0.11.0',
 'sqlalchemy-bigquery>=1.4,<2.0',
 'sqlparse>=0.3.1,<0.5.0',
 'typer[all]>=0.4,<0.8']

extras_require = \
{'dash': ['Werkzeug==2.2.2',
          'dash[testing]==2.7.1',
          'dash-cytoscape==0.3.0',
          'dash-bootstrap-components>=1.1.0,<2.0.0',
          'Authlib>=1.0',
          'dash-ace>=0.2.1,<0.3.0',
          'dash-extensions>=0.1.10,<0.2.0',
          'dash-mantine-components>=0.10.2,<0.12.0',
          'prometheus-flask-exporter==0.21.0',
          'gunicorn>=20.1.0,<21.0.0'],
 'feature-store': ['feast[gcp,redis]==0.26.0',
                   'prometheus-fastapi-instrumentator>=5.8.1,<6.0.0']}

entry_points = \
{'console_scripts': ['amora = amora.cli:main'],
 'pytest11': ['amora = amora.tests.pytest_plugin']}

setup_kwargs = {
    'name': 'amora',
    'version': '0.1.22',
    'description': 'Amora Data Build Tool',
    'long_description': 'None',
    'author': 'diogommartins',
    'author_email': 'diogo.martins@stone.com.br',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
