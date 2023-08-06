import re
from sys import argv

from setuptools import setup, find_packages

requires = ["requests", "pycryptodome==3.10.1", "urllib3", "tqdm", "aiohttp", "rich", "websocket-client"]
version = "6.0.5"


## robikalo

setup(
        # the name must match the folder name 'verysimplemodule'
        name="robikalo", 
        version='8.0.1',
        author="Kazem Mirzaei",
        author_email="k90mirzaei@gmail.com",
        description='My first Python package',
        long_description='My first Python package with a slightly longer description',
        packages=find_packages(),
        
        # add any additional packages that 
        # needs to be installed along with your package.
        install_requires=[], 
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
        ]
)