# -*- coding: utf-8 -*-
from setuptools import setup

long_description = None
INSTALL_REQUIRES = [
    "pytailwindcss>=0.1.4",
]
ENTRY_POINTS = {
    "lektor.plugins": [
        "tailwind = lektor_tailwind:TailwindPlugin",
    ],
}

setup_kwargs = {
    "name": "lektor-tailwind",
    "version": "0.1",
    "description": "",
    "long_description": long_description,
    "license": "MIT",
    "author": "",
    "author_email": "Frost Ming <mianghong@gmail.com>",
    "maintainer": None,
    "maintainer_email": None,
    "url": "",
    "package_data": {"": ["*"]},
    "install_requires": INSTALL_REQUIRES,
    "python_requires": ">=3.8",
    "entry_points": ENTRY_POINTS,
}


setup(**setup_kwargs)
