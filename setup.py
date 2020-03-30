#!/usr/bin/env python

from setuptools import setup

setup(name='az-account-switcher',
      version='0.0.1',
      description='Utility to switch Azure subscriptions',
      author='Alexander Bij',
      url='https://docs.microsoft.com/cli/azure/manage-azure-subscriptions-azure-cli',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      install_requires=[
          'azure-common',
          'click'
      ],
      entry_points='''
          [console_scripts]
          az-switch=az_account_switcher:main
      ''',
)
