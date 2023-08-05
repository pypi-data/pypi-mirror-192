from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'package to convert units'
LONG_DESCRIPTION = 'package to convert units long version'

# Setting up
setup(
    name="unitcvtr",
    version=VERSION,
    author="UndefinedRekian (Rekian Dewandaru)",
    author_email="<rekian.fajar@aqi.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'unit', 'math', 'convert'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)