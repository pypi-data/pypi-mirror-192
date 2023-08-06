from setuptools import setup
from setuptools import find_packages


VERSION = '0.0.1'

setup(
    name='duoyuantongji',  # package name
    version=VERSION,  # package version
    description='my package test',  # package description
    packages=find_packages(),
    zip_safe=False,
)
