#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: setup
@time: 2020/12/7
@email: coderflying@163.com
@desc: 
"""
from distutils.core import setup

# This is a list of files to install, and where
# (relative to the 'root' dir, where setup.py is)
# You could be more specific.
from pkgutil import walk_packages
from setuptools import find_packages

files = ["things/*"]



install_requires = [
    'pika>=1.2.0',
    'requests>=2.25.1',
    'Scrapy==2.5.1',
]

setup(name="scrapy-toolset",
      version="0.0.39",
      description="noting",
      author="coder-fly",
      author_email="coderflying@163.com",
      url="https://github.com/coder-fly",
      packages=list(find_packages('src')),
      package_dir={'': 'src'},
      long_description="""nothing""",
      install_requires=install_requires,
      python_requires='>=3.6',
      license="MIT",
      #
      # This next part it for the Cheese Shop, look a little down the page.
      # classifiers = []
      # python setup.py sdist build
      # twine upload dist/*
      )