from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Complementary Data Analysis Library for Pandas'

# Setting up
setup(
    name="dafy",
    version=VERSION,
    author="Miguel Saraiva",
    author_email="<miguelmmsaraiva1@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'numpy'],
    keywords=['python', 'data', 'analysis', 'pandas', 'data analysis'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)