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
        self.data_configs = data_configs

    @staticmethod
    def url_open(mirror):
        """ Read the url and return the changelog.txt file. """
        changelog_txt = ''
        try:
            http = urllib3.PoolManager()
            con = http.request('GET', mirror)
            changelog_txt = con.data.decode()
        except KeyError:
            print('SUN: error: ftp mirror not supported')

        return changelog_txt

    @staticmethod
    def read_file(registry):
        """ Return reading file. """
        if os.path.isfile(registry):
            with open(registry, 'r', encoding='utf-8', errors='ignore') as file_txt:
                return file_txt.read()

        print(f"\nNo '{registry.split('/')[-1]}' file was found.\n")

    def slack_ver(self):
        """ Open a file and read the Slackware version. """
        dist = self.read_file('/etc/slackware-version')
        sv = re.findall(r'\d+', dist)

        if len(sv) > 2:
            version = ('.'.join(sv[:2]))
        else:
            version = ('.'.join(sv))

        return dist.split()[0], version

    @staticmethod
    def read_mirrors_file(mirrors):
        """ Read a mirror from the /etc/slackpkg/mirrors file. """
        for mirror in mirrors.splitlines():

            if mirror and not mirror.startswith('#'):
                return mirror.lstrip()

        return ''

    def mirror_url(self):
        """ Return the mirror url. """
        mirror = self.read_mirrors_file(self.read_file(f'{self.data_configs["etc_slackpkg"]}mirrors'))

        if self.alter_mirror:
            mirror = self.alter_mirror

        if not mirror:
            print('You do not have any http/s mirror selected in /etc/slackpkg/'
                  'mirrors.\nPlease edit that file and uncomment ONE http/s mirror\n '
                  'or edit the /etc/sun/sun.toml configuration file.')
            return ''

        elif mirror.startswith('ftp'):
            print('Please select an http/s mirror not ftp.')
            return ''

        return f'{mirror}{self.changelog_file}'

    def fetch(self):
        """ Read the ChangeLog.txt files and counts the packages. """
        days = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
        mirror_changelog_txt = self.mirror_url()
        local_date = ''

        if mirror_changelog_txt:
            mirror_changelog_txt = self.url_open(mirror_changelog_txt)
            local_changelog_txt = self.read_file(f'{self.library_path}{self.changelog_file}')

            for line in local_changelog_txt.splitlines():
                if line.startswith(days):
                    local_date = line.strip()
                    break

            # Compare two dates local and mirror from ChangeLogs files.
            for line in mirror_changelog_txt.splitlines():
                if local_date == line.strip():
                    break

                # This condition checks the packages
                if re.findall(self.regex_packages, line):
                    yield line.split('/')[-1]

    def os_info(self):
        """ Get the OS info. """
        stype = 'Stable'
        mir = self.mirror_url()

        if mir and 'current' in mir:
            stype = 'Current'

        info = (
            f'User: {getpass.getuser()}\n'
            f'OS: {self.slack_ver()[0]}\n'
            f'Version: {self.slack_ver()[1]}\n'
            f'Type: {stype}\n'
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
