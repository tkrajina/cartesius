#!/usr/bin/python

# Copyright 2011 Tomo Krajina
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools as mod_setuptools

import cartesius as mod_cartesius

mod_setuptools.setup(
    name = 'cartesius',
    version = mod_cartesius.__version__,
    description = 'Cartesius 2D coordinate system drawing library',
    license = 'Apache License, Version 2.0',
    author = 'Tomo Krajina',
    author_email = 'tkrajina@gmail.com',
    url = 'http://tkrajina.github.com/cartesius/',
    packages = ['cartesius', 'cartesius/fonts'],
    package_data = {'': ['*.ttf']},
    include_package_data = True,
)

