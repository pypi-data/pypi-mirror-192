from setuptools import setup, find_packages

VERSION = '1.4'
DESCRIPTION = ''
LONG_DESCRIPTION = ''

setup(
    name='miquant',
    version=VERSION,
    packages=find_packages(),
    install_requires=['pandas']
)

