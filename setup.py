#!/usr/bin/env python3
from setuptools import setup, find_packages


setup(
    name='cmdb_neo',
    version='0.0.1',
    author='zhanghaoran',
    author_email='haoranzeus@163.com',
    description='CMDB based on neo4j',
    packages=find_packages(exclude=['tests']),
    install_requires=['flask', 'flask-restful', 'neo4j-driver', 'pymysql']
)
