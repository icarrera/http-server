# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='echo server',
    description='A Python application stufff here ',
    version=0.1,
    author='Norton Pengra and Iris Carrera',
    license='MIT',
    py_modules=['client', 'server'],
    package_dir={'': 'src'},
    extras_require={'test': ['pytest', 'pytest-xdist', 'tox']},
    install_requires=['gevent'],
)
