# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['csplint']
install_requires = \
['tomli']

entry_points = \
{'flake8.extension': ['CSP = csplint:CSPPlugin']}

setup_kwargs = {
    'name': 'csplint',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Stanislav Zmiev',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
