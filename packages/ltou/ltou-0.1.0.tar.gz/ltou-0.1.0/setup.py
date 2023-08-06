# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ltou',
 'ltou.template',
 'ltou.template.hooks',
 'ltou.template.{{cookiecutter.project_name}}',
 'ltou.template.{{cookiecutter.project_name}}.app',
 'ltou.template.{{cookiecutter.project_name}}.app.api',
 'ltou.template.{{cookiecutter.project_name}}.app.api.endpoints',
 'ltou.template.{{cookiecutter.project_name}}.app.cli',
 'ltou.template.{{cookiecutter.project_name}}.app.core',
 'ltou.template.{{cookiecutter.project_name}}.app.crud',
 'ltou.template.{{cookiecutter.project_name}}.app.middlewares',
 'ltou.template.{{cookiecutter.project_name}}.app.models',
 'ltou.template.{{cookiecutter.project_name}}.app.move_db_beanie',
 'ltou.template.{{cookiecutter.project_name}}.app.move_db_mongo',
 'ltou.template.{{cookiecutter.project_name}}.app.move_db_sa',
 'ltou.template.{{cookiecutter.project_name}}.app.move_db_sqlmodel',
 'ltou.template.{{cookiecutter.project_name}}.app.move_db_tortoise',
 'ltou.template.{{cookiecutter.project_name}}.app.move_worker',
 'ltou.template.{{cookiecutter.project_name}}.app.schemas',
 'ltou.template.{{cookiecutter.project_name}}.app.tests',
 'ltou.template.{{cookiecutter.project_name}}.app.utils',
 'ltou.template.{{cookiecutter.project_name}}.move_alembic',
 'ltou.template.{{cookiecutter.project_name}}.move_alembic.versions']

package_data = \
{'': ['*'],
 'ltou.template': ['.github/workflows/*'],
 'ltou.template.{{cookiecutter.project_name}}': ['deploy/*'],
 'ltou.template.{{cookiecutter.project_name}}.app': ['docker/*', 'scripts/*']}

install_requires = \
['asyncpg>=0.27.0,<0.28.0',
 'click>=8.1.3,<9.0.0',
 'cookiecutter>=1.7.3,<2.0.0',
 'greenlet==2.0.2',
 'loguru>=0.6.0,<0.7.0',
 'pre-commit>=3.0.4,<4.0.0',
 'prompt-toolkit>=3.0.36,<4.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'pytest>=7.2.1,<8.0.0',
 'pytz>=2022.7.1,<2023.0.0',
 'simple-term-menu>=1.5.2,<2.0.0',
 'sqlalchemy>=2.0.2,<3.0.0',
 'termcolor>=2.2.0,<3.0.0',
 'tortoise>=0.1.1,<0.2.0',
 'uvicorn>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['ltou = ltou.__main__:main']}

setup_kwargs = {
    'name': 'ltou',
    'version': '0.1.0',
    'description': "Like 'cargo new' cli creat fastapi project",
    'long_description': '<h1 align="center">\n  LTOU 🦖\n</h1>\n\n<p align="center">\n  <strong>Create Fastapi App CLI</strong>\n<br /> Supercharged Productivity⚡️\n</p>\n\n\n\n<p align="center">✨Create a new production-ready project and <b>deploy automation</b> (Docker,CICD) by running  ltou command.\n<br/><br/>Focus on <b>writing</b> code and <b>thinking</b> of business-logic! Don\'t Panic!  The CLI will take care of the rest. Drink More coffee ☕️ and Ship More🛳️ </p>\n\n## ⚡️ Quick start\nYou can install it directly from pypi with pip.\n```shell\npython3 -m pip install ltou\n```\nLet\'s create a new project via interactive console UI (or CUI for short) in current folder:\n```shell\nltou\n```\n🍪 That\'s all you need to know to start! 🍪 \n\n## ⚡️ Features\nOne of the coolest features is that this project is extremely configurable(**as-plugins**).\nYou can choose between different databases and even ORMs, or\nyou can even generate a project without a database!\nCurrently, SQLAlchemy2.0(1.4+), SqlModel, Beanie  and Tortoise  are supported.\n\nThis project can run as TUI or CLI and has excellent code documentation.\n\nOut-of-the-box Feature:\n- Different databases support;\n- Different ORMs support;\n- Optional redis support;\n- Optional rabbitmq support;\n- Optional CI/CD;\n- Optional Sentry integration;\n- Optional Loguru logger;\n- Optional Celery(flower);\n- Pre-commit integration;\n- Some utils plugins\n- ...\n\n\n## ⚡️ Thinks \n \nthis \'**ltou**\' short name is inspired by ["The Last of Us"](https://en.wikipedia.org/wiki/The_Last_of_Us).\n\n ',
    'author': 'hiro',
    'author_email': 'yidiyu0507s@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
