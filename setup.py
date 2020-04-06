#!/usr/bin/env python

from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(name='az-account-switcher',
      version='0.0.5',
      description='Utility to switch Azure subscriptions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Alexander Bij',
      author_email='Alexander.Bij@gmail.com',
      url='https://github.com/abij/az-account-switcher',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      packages=['az_account_switcher'],
      python_requires='>3.6',
      install_requires=[
          'azure-common',
          'azure-cli-core',
          'click'
      ],
      entry_points='''
          [console_scripts]
          az-switch=az_account_switcher:main
      ''',
      )
