##
#     Project: gExtractWinIcons
# Description: Extract cursors and icons from MS Windows resource files.
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2009-2022 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import configparser
import optparse
import os
import os.path
import time

from gextractwinicons.constants import (FILE_SETTINGS_NEW,
                                        VERBOSE_LEVEL_MAX,
                                        VERBOSE_LEVEL_NORMAL,
                                        VERBOSE_LEVEL_QUIET)

SECTION_MAINWIN = 'main window'


class Settings(object):
    def __init__(self):
        self.settings = {}

        # Command line options and arguments
        parser = optparse.OptionParser(usage='usage: %prog [options]')
        parser.set_defaults(verbose_level=VERBOSE_LEVEL_NORMAL)
        parser.add_option('-v', '--verbose', dest='verbose_level',
                          action='store_const', const=VERBOSE_LEVEL_MAX,
                          help='show error and information messages')
        parser.add_option('-q', '--quiet', dest='verbose_level',
                          action='store_const', const=VERBOSE_LEVEL_QUIET,
                          help='hide error and information messages')
        parser.add_option('-d', '--destination',
                          help='set initial destination folder')
        parser.add_option('-f', '--filename',
                          help='set resources filename')
        parser.add_option('-r', '--refresh', action='store_true',
                          help='automatically refresh resources list '
                               'if -f specified')
        parser.add_option('-n', '--nofreeze', action='store_true',
                          help='do not freeze the treeview during '
                               'the refresh (slower)')
        (self.options, self.arguments) = parser.parse_args()
        if self.options.refresh and not self.options.filename:
            parser.error('option -r requires filename specified with -f')
        if self.options.filename and not os.path.isfile(self.options.filename):
            parser.error(
                'the specified file "%s" is not valid' % self.options.filename)
        # Parse settings from the configuration file
        self.config = configparser.RawConfigParser()
        # Allow saving in case sensitive (useful for machine names)
        self.config.optionxform = str
        # Determine which filename to use for settings
        self.filename = FILE_SETTINGS_NEW
        if self.filename:
            self.logText('Loading settings from %s' % self.filename,
                         VERBOSE_LEVEL_NORMAL)
            self.config.read(self.filename)

    def load(self):
        "Load window settings"
        if self.config.has_section(SECTION_MAINWIN):
            self.logText('Retrieving window settings', VERBOSE_LEVEL_NORMAL)
            # Retrieve window position and size
            if self.config.has_option(SECTION_MAINWIN, 'left'):
                self.settings['left'] = self.config.getint(SECTION_MAINWIN,
                                                           'left')
            if self.config.has_option(SECTION_MAINWIN, 'top'):
                self.settings['top'] = self.config.getint(SECTION_MAINWIN,
                                                          'top')
            if self.config.has_option(SECTION_MAINWIN, 'width'):
                self.settings['width'] = self.config.getint(SECTION_MAINWIN,
                                                            'width')
            if self.config.has_option(SECTION_MAINWIN, 'height'):
                self.settings['height'] = self.config.getint(SECTION_MAINWIN,
                                                             'height')

    def get_value(self, name, default=None):
        return self.settings.get(name, default)

    def set_sizes(self, winParent):
        "Save configuration for main window"
        # Main window settings section
        self.logText('Saving window settings', VERBOSE_LEVEL_NORMAL)
        if not self.config.has_section(SECTION_MAINWIN):
            self.config.add_section(SECTION_MAINWIN)
        # Window position
        position = winParent.get_position()
        self.config.set(SECTION_MAINWIN, 'left', position[0])
        self.config.set(SECTION_MAINWIN, 'top', position[1])
        # Window size
        size = winParent.get_size()
        self.config.set(SECTION_MAINWIN, 'width', size[0])
        self.config.set(SECTION_MAINWIN, 'height', size[1])

    def save(self):
        "Save the whole configuration"
        # Always save the settings in the new configuration file
        file_settings = open(FILE_SETTINGS_NEW, mode='w')
        self.logText('Saving settings to %s' % FILE_SETTINGS_NEW,
                     VERBOSE_LEVEL_NORMAL)
        self.config.write(file_settings)
        file_settings.close()

    def logText(self, text, verbose_level=VERBOSE_LEVEL_NORMAL):
        "Print a text with current date and time based on verbose level"
        if verbose_level <= self.options.verbose_level:
            print
            '[%s] %s' % (time.strftime('%Y/%m/%d %H:%M:%S'), text)

    def get_home_directory(self):
        "Return the user home directory"
        return os.path.expanduser('~')
