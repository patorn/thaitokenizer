# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='thai-sentiment',
    version='0.1.0',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='Patorn Utenpattanun',
    author_email='patorn.u@gmail.com',
    url='https://github.com/patorn/thai-sentiment',
    license=license,
    tests_require=[
        'pytest',
        'pylint',
        'coverage'
    ]
)
