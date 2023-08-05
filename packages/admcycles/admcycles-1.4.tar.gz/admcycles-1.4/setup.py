## -*- encoding: utf-8 -*-
import os
import sys
from setuptools import setup
from codecs import open

# Get information from separate files (README, VERSION)
def readfile(filename):
    with open(filename,  encoding="utf-8") as f:
        return f.read()

setup(
    name="admcycles",
    version=readfile("VERSION").strip(), # the VERSION file is shared with the documentation
    description="Tautological ring on Mbar_g,n",
    long_description=readfile("README.rst"), # get the long description from the README
    url="https://gitlab.com/modulispaces/admcycles",
    author="Vincent Delecroix, Aaron Pixton, Johannes Schmitt, Jason van Zelm, Jonathan Zachhuber",
    author_email="jo314schmitt@gmail.com",
    license="GPLv2+",
    classifiers=[
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Science/Research",
      "Topic :: Scientific/Engineering :: Mathematics",
      "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
      "Programming Language :: Python :: 3"
    ], # classifiers list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords = "SageMath geometry moduli space curve",
    packages = ["admcycles", "admcycles/DR", "admcycles/diffstrata"],
)
