#!/usr/bin/python3
# -*- coding: utf-8 -*-

# configs.py is a part of sun.

# Copyright 2015-2023 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# sun is a tray notification applet for informing about
# package updates in Slackware.

# https://gitlab.com/dslackw/sun

# sun is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import os
import tomli

from dataclasses import dataclass
from sun.__metadata__ import data_configs


@dataclass
class Configs:

    config_file: str = 'sun.toml'

    # Daemon manage time configs.
    interval: int = 60
    standby: int = 3

    # Regex pattern.
    regex_packages: str = 'Upgraded[.]|Rebuilt[.]|Added[.]|Removed[.]'

    # Library configs.
    changelog_file: str = f'{data_configs["changelog_txt"]}'
    library_path: str = f'{data_configs["var_lib_slackpkg"]}{changelog_file}'

    # Alternative mirror.
    alter_mirror: str = ''

    # Configuration file.
    config_file = f'{data_configs["conf_path"]}{config_file}'

    # Load configuration from /etc/sun/sun.toml file.
    try:
        if os.path.isfile(config_file):
            with open(config_file, 'rb') as conf:
                configs = tomli.load(conf)
    except tomli.TOMLDecodeError as error:
        print("ValueError: {error}: in the configuration file '/etc/sun/sun.toml'")

    if configs:
        try:
            interval: int = configs['time']['INTERVAL']
            standby: int = configs['time']['STANDBY']
            regex_packages: str = configs['regex']['PACKAGES']

            changelog_file: str = configs['library']['CHANGELOG_FILE']
            library_path: str = configs['library']['LIBRARY_PATH']
            alter_mirror: str = configs['mirror']['HTTP_MIRROR']
        except KeyError as error:
            print(f"KeyError: {error}: in the configuration file '/etc/sun/sun.toml'.")
