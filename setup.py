#!/usr/bin/env python3
from setuptools import setup

setup(
    name='filtercss',
    version='0.0.2',
    author='Jan Jancar',
    author_email='johny@neuromancer.sk',
    url='https://github.com/J08nY/filtercss/',
    license='MIT',
    description='Tool for filtering unused CSS.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['filtercss'],
    install_requires=[
        'tinycss2',
        'beautifulsoup4',
        'lxml'
    ],
    python_requires='>=3.8'
)
