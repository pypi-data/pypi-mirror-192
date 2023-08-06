# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sqla_wrapper', 'sqla_wrapper.cli']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.9,<2.0', 'sqlalchemy>=2.0,<3.0']

setup_kwargs = {
    'name': 'sqla-wrapper',
    'version': '6.0.0',
    'description': 'A framework-independent modern wrapper for SQLAlchemy & Alembic',
    'long_description': '![SQLA-Wrapper](header.png)\n\nA friendly wrapper for [modern SQLAlchemy](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) (v1.4 or later) and Alembic.\n\n**Documentation:** https://sqla-wrapper.scaletti.dev/\n\nIncludes:\n\n- A SQLAlchemy wrapper, that does all the SQLAlchemy setup and gives you:\n    - A scoped session extended with some useful active-record-like methods.\n    - A declarative base class.\n    - A helper for performant testing with a real database.\n\n    ```python\n    from sqla_wrapper import SQLAlchemy\n\n    db = SQLAlchemy("sqlite:///db.sqlite", **options)\n    # You can also use separated host, name, etc.\n    # db = SQLAlchemy(user=…, password=…, host=…, port=…, name=…)\n    ```\n\n- An Alembic wrapper that loads the config from your application instead of from separated `alembic.ini` and `env.py` files.\n\n    ```python\n    from sqla_wrapper import Alembic, SQLAlchemy\n\n    db = SQLAlchemy(…)\n    alembic = Alembic(db, "db/migrations")\n    ```\n\n',
    'author': 'Juan-Pablo Scaletti',
    'author_email': 'juanpablo@jpscaletti.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://sqla-wrapper.scaletti.dev/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
