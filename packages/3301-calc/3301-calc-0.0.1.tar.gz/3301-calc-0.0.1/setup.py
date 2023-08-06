# -*- coding: utf-8 -*-

from setuptools import setup

version = '0.0.1'


setup(
    name = "3301-calc",
    packages = ["calc"],
    entry_points = {
        "console_scripts": ['calculate = calc.calc:main']
        },
    version = version,
    description = "Python command line application bare bones template.",
    long_description = "README File",
    author = "Anurag Kumar Singh",
    author_email = "anurag3301.0x0@gmail.com",
    )
