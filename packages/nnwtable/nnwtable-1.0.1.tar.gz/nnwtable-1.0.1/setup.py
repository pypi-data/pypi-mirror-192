#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: d.i.glukhikh
:license: GNU General Public License v3.0, see LICENSE file
:copyright: (c) 2023 d.i.glukhikh
"""

version = '1.0.1'

#with open('README.md', encoding='utf-8') as f:
    #long_description = f.read()

setup(
    name='nnwtable',
    version=version,

    author='d.i.glukhikh',
    author_email='gluhihdmitry@gmail.ru',

    description=(
        u'ensamble neural network for table data classification'
    ),
    #long_description=long_description,
    #long_description_content_type='text/markdown',

    url='https://github.com/diglukhikh/neural-network-for-classifier',
    download_url='https://github.com/diglukhikh/neural-network-for-classifier/raw/main/archive1/main.zip',

    license='GNU General Public License v3.0',

    packages=['nnwtable'],
    install_requires=['keras', "numpy"],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)