#!/usr/bin/python3
# -*- coding: utf-8 -*-

# daemon.py is a part of sun.

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


"""
 ____  _   _ _   _
/ ___|| | | | \ | |
\___ \| | | |  \| |
 ___) | |_| | |\  |
|____/ \___/|_| \_|

"""


import time
import notify2
import subprocess
from sun.configs import Configs
from sun.utils import Utilities
from sun.__metadata__ import __all__, data_configs


class Notify(Configs):
    """ Main notify Class. """

    def __init__(self):
        super(Configs, self).__init__()

        notify2.uninit()
        notify2.init('sun')
        utils = Utilities()

        self.data_configs = data_configs
        self.count_packages: int = len(list(utils.fetch()))

        self.summary: str = f"{' ' * 10}Software Updates"
        self.message: str = f"{' ' * 3}{self.count_packages} Software updates are available\n"

        self.icon: str = f'{self.data_configs["icon_path"]}{__all__}.png'

        self.n = notify2.Notification(self.summary, self.message, self.icon)
        self.n.set_timeout(60000 * self.standby)

    @staticmethod
    def gtk_loaded():
        """ Check if gtk icon running. """
        output = subprocess.getoutput('ps -a')
        if 'sun_gtk' in output:
            return True

    def show_notify(self):
        """ Startup dbus message if packages. """
        if self.count_packages > 0 and self.gtk_loaded():
            self.n.show()  # show notification


def main():

    while True:
        utils = Utilities()
        count_packages = len(list(utils.fetch()))

        if count_packages > 0:
            n = Notify()
            n.show_notify()
            time.sleep(60 * Configs.interval)


if __name__ == '__main__':
    main()
