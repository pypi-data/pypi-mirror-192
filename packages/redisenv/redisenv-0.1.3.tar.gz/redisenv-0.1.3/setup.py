# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redisenv', 'redisenv.commands']

package_data = \
{'': ['*'], 'redisenv': ['templates/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['redisenv = redisenv:__main__.main']}

setup_kwargs = {
    'name': 'redisenv',
    'version': '0.1.3',
    'description': 'A tool for building redis test environments',
    'long_description': '# redisenv\n\n[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)\n[![pypi](https://badge.fury.io/py/redisenv.svg)](https://pypi.org/project/redisenv/)\n[![CI](https://github.com/RedisLabsModules/redisenv/actions/workflows/integration.yml/badge.svg)](https://github.com/RedisLabsModules/redisenv/actions/workflows/integration.yml)\n\nredisenv is library that makes generating redis test environments easier. This tool generates [docker-compose](https://docs.docker.com/compose/) files, and runs all instances within docker.  Generated docker instances select a random port, based on the available free ports, and when running ```redisenv ports```, a JSON parse-able string of the build connections is outputted.\n\nCurrently redisenv supports:\n\n* Redis standalone\n\n* Redis Sentinel\n\n* Redis Clusters\n\n* Redis masters with replicas\n\nNote: Today Redis Standalone supports redis-stack, but nothing else does\n\n----\n\n## Installation\n\n### Requirements\n\n* Python >= 3.7\n\n* docker-compose\n\n* docker\n\n## Usage\n\nList options. Note, each sub command accepts its own ```--help```\n\n```bash\nredisenv --help\n```\n\nStart an environment named foo, with one container:\n\n```bash\nredisenv --name foo standalone create --nodes 1\n```\n\nStart an environment with the redisbloom module, downloaded into a folder named modules. Note - you need the full *local* path to the directory.\n\n```bash\nredisenv --name foo standalone create -n 1 -M `pwd`/modules /modules -o "--loadmodule /modules/redisbloom.so"\n```\n\nDestroy the environment named foo:\n\n```bash\nredisenv --name foo destroy\n```\n',
    'author': 'Redis OSS',
    'author_email': 'oss@redis.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
