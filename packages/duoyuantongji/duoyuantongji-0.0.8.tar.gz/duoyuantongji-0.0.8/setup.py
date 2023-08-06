from setuptools import setup
from setuptools import find_packages


VERSION = '0.0.8'

setup(
    name='duoyuantongji',  # package name
    version=VERSION,  # package version
    description='my package test',  # package description
    packages=find_packages('src'),
    package_data={"evatool.resource": [
        "*.json", "*.conf", "*.html"], "evatool.bin": ["*"]},
    # packages=find_packages(exclude=["test", "test.*"]),
    zip_safe=False,
)
