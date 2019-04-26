# Copyright 2018 AT&T Intellectual Property.  All other rights reserved.
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

from setuptools import setup
from setuptools import find_packages

setup(
    name='spyglass_plugin_xls',
    version='0.0.1',
    description='Excel data source plugin for Spyglass',
    url='https://opendev.org/airship/spyglass-plugin-xls',
    python_requires='>=3.5.0',
    license='Apache 2.0',
    packages=find_packages(),
    install_requires=[
        'PyYAML==3.12',
        'openpyxl==2.5.4',
    ],
    dependency_links=[
        'git+https://opendev.org/airship/spyglass.git',
    ],
    include_package_data=True,
)
