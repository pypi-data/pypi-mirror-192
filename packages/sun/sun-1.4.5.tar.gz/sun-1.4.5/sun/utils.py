#!/usr/bin/python3
# -*- coding: utf-8 -*-

# utils.py is a part of sun.

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
import re
import getpass
import urllib3
from sun.configs import Configs
from sun.__metadata__ import data_configs


class Utilities(Configs):

    def __init__(self):
        super(Configs, self).__init__()
        self.data_configs: dict = data_configs

    @staticmethod
    def url_open(mirror):
        """ Read the url and return the changelog.txt file. """
        log_txt: str = ''
        try:
            http = urllib3.PoolManager()
            con = http.request('GET', mirror)
            log_txt = con.data.decode()
        except KeyError:
            print('SUN: error: ftp mirror not supported')

        return log_txt

    @staticmethod
    def read_file(registry):
        """ Return reading file. """
        if os.path.isfile(registry):
            with open(registry, 'r', encoding='utf-8', errors='ignore') as file_txt:
                return file_txt.read()
        else:
            print(f"\nNo '{registry.split('/')[-1]}' file was found.\n")

    def slack_ver(self):
        """ Reads the Slackware version. """
        distribution: str = self.read_file('/etc/slackware-version')
        slackware_version: list = re.findall(r'\d+', distribution)

        return distribution.split()[0], '.'.join(slackware_version)

    def fetch(self):
        """ Read the ChangeLog.txt files and counts the packages. """
        days: tuple = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
        local_date: str = ''

        for repository in self.repositories:

            mirror: str = repository['HTTP_MIRROR']

            if mirror:

                if not mirror.endswith('/'):
                    mirror: str = f'{mirror}/'

                mirror_log_txt: str = self.url_open(f"{mirror}{repository['LOG_FILE']}")
                local_log_txt: str = self.read_file(f"{repository['LOG_PATH']}{repository['LOG_FILE']}")

                for line in local_log_txt.splitlines():
                    if line.startswith(days):
                        local_date: str = line.strip()
                        break

                # Compare two dates local and mirror from ChangeLogs files.
                for line in mirror_log_txt.splitlines():
                    if local_date == line.strip():
                        break

                    # This condition checks the packages
                    if re.findall(repository['PATTERN'], line):

                        # Some patches for Slackware repository.
                        if repository['NAME'] == 'Slackware':
                            line = re.sub(repository["PATTERN"], '', line)
                            line = line.replace(':', '').strip()

                            # Fixed line for linux patches Upgraded.
                            if line.startswith('patches/packages/linux'):
                                line = line.split("/")[-2]

                        yield f'{repository["NAME"]}: {line.split("/")[-1]}'

    def os_info(self):
        """ Get the OS info. """

        info: str = (
            f'User: {getpass.getuser()}\n'
            f'OS: {self.slack_ver()[0]}\n'
            f'Version: {self.slack_ver()[1]}\n'
            f'Arch: {self.data_configs["arch"]}\n'
            f'Packages: {len(os.listdir(self.data_configs["pkg_path"]))}\n'
            f'Kernel: {self.data_configs["kernel"]}\n'
            f'Uptime: {self.data_configs["uptime"]}\n'
            '[Memory]\n'
            f'Free: {self.data_configs["mem"][9]}, Used: {self.data_configs["mem"][8]}, '
            f'Total: {self.data_configs["mem"][7]}\n'
            '[Disk]\n'
            f'Free: {self.data_configs["disk"][2] // (2**30)}Gi, Used: '
            f'{self.data_configs["disk"][1] // (2**30)}Gi, '
            f'Total: {self.data_configs["disk"][0] // (2**30)}Gi\n'
            f'[Processor]\n'
            f'CPU: {self.data_configs["cpu"]}'
            )

        return info
