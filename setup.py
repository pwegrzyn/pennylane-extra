# Copyright 2019 Xanadu Quantum Technologies Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#!/usr/bin/env python3

import sys
import os
from setuptools import setup

with open("pennylane_extra/_version.py") as f:
    version = f.readlines()[-1].split()[-1].strip("\"'")

# Put pip installation requirements here.
# Requirements should be as minimal as possible.
# Avoid pinning, and use minimum version numbers
# only where required.
requirements = ["pennylane>=0.8.1", "PennyLane-qiskit>=0.8.2"]

info = {
    # 'name' is the name that will be used by pip for installation
    "name": "PennyLane-Extra",
    "version": version,
    "maintainer": "G. Frejek, P. Wegrzyn",
    "maintainer_email": "gfrejek@gmail.com, wegpat@gmail.com",
    "url": "https://github.com/pwegrzyn/pennylane-extra",
    "license": "Apache License 2.0",
    "packages": [
        # The name of the folder containing the plugin.
        # This is the name that will be used when importing
        # the plugin in Python.
        "pennylane_extra"
    ],
    "entry_points": {"pennylane.plugins": ["extra = pennylane_extra"]},
    # Place a one line description here. This will be shown by pip
    "description": "Extension to PennyLane adding various miscellaneous features",
    "long_description": open("README.rst").read(),
    # The name of the folder containing the plugin
    "provides": ["pennylane_extra"],
    "install_requires": requirements,
    'command_options': {
        'build_sphinx': {
            'version': ('setup.py', version),
            'release': ('setup.py', version)}}
}

classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: POSIX",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python",
    # Make sure to specify here the versions of Python supported
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Scientific/Engineering :: Physics",
]

setup(classifiers=classifiers, **(info))
