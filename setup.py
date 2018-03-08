# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='thaitokenizer',
    version='0.1.0',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='Patorn Utenpattanun',
    author_email='patorn.u@gmail.com',
    url='https://github.com/patorn/thaitokenizer',
    license=license,
    packages=find_packages(exclude=['notebooks']),
    include_package_data=True,
    tests_require=[
        'pytest',
        'pylint',
        'coverage'
    ]
)
