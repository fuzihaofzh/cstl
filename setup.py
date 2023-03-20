#!/usr/bin/env python
from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
from CSTL.version import __version__

setup(
    name='CSTL',
    version=__version__,
    description='The C++ Standard Template Library (STL) for Python',
    url='https://github.com/fuzihaofzh/CSTL',
    author='',
    author_email='',
    license='',
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
    keywords='C++ STL List Dict Set',
    packages = find_packages(),  
    package_data={'': ['_CSTL.so']},
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True
)