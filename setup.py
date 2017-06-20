#!/usr/bin/env python

from setuptools import setup

setup(
    name         = "blynk-library-python",
    version      = "0.1.0", #blynk.lib.__version__
    description  = "Blynk library",
    platforms    = "any",
    url          = "http://www.blynk.cc",
    license      = "MIT",
    author       = "Volodymyr Shymanskyy",
    author_email = "vshymanskyi@gmail.com",

    py_modules   = ['BlynkLib'],

    classifiers  = [
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X"
    ]
)
