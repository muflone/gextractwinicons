##
#     Project: gExtractWinIcons
# Description: Extract cursors and icons from MS Windows resource files
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

import pathlib
import sys

from xdg import BaseDirectory


# Application constants
APP_NAME = 'gExtractWinIcons'
APP_VERSION = '0.5.2'
APP_DESCRIPTION = 'Extract cursors and icons from MS Windows resource files'
APP_DOMAIN = 'gextractwinicons'
APP_AUTHOR = 'Fabio Castelli'
APP_AUTHOR_EMAIL = 'muflone@muflone.com'
APP_COPYRIGHT = f'Copyright 2009-2022 {APP_AUTHOR}'
APP_ID = f'{APP_DOMAIN}.muflone.com'
URL_AUTHOR = 'http://www.muflone.com/'
URL_APPLICATION = f'{URL_AUTHOR}{APP_DOMAIN}/'
URL_SOURCES = f'https://github.com/muflone/{APP_DOMAIN}/'
URL_TRANSLATIONS = f'https://explore.transifex.com/muflone/{APP_DOMAIN}/'
# Other constants
VERBOSE_LEVEL_QUIET = 0
VERBOSE_LEVEL_NORMAL = 1
VERBOSE_LEVEL_MAX = 2
# Resources type
RESOURCE_TYPE_CURSOR = 1
RESOURCE_TYPE_BITMAP = 2
RESOURCE_TYPE_ICON = 3
RESOURCE_TYPE_MENU = 4
RESOURCE_TYPE_DIALOG = 5
RESOURCE_TYPE_STRING = 6
RESOURCE_TYPE_FONTDIR = 7
RESOURCE_TYPE_FONT = 8
RESOURCE_TYPE_ACCELERATOR = 9
RESOURCE_TYPE_RCDATA = 10
RESOURCE_TYPE_MESSAGELIST = 11
RESOURCE_TYPE_GROUP_CURSOR = 12
RESOURCE_TYPE_GROUP_ICON = 14
RESOURCE_TYPE_VERSION = 16
RESOURCE_TYPE_DLGINCLUDE = 17
RESOURCE_TYPE_PLUGPLAY = 19
RESOURCE_TYPE_VXD = 20
RESOURCE_TYPE_ANICURSOR = 21
RESOURCE_TYPE_ANIICON = 22

# Paths constants
path_xdg_data_home = pathlib.Path(BaseDirectory.xdg_data_home)
icon_name = f'{APP_DOMAIN}.png'
if (pathlib.Path('data') / icon_name).is_file():
    # Use relative paths
    DIR_PREFIX = pathlib.Path('data').parent.absolute()
    DIR_LOCALE = DIR_PREFIX / 'locale'
    DIR_DOCS = DIR_PREFIX / 'doc'
elif (path_xdg_data_home / APP_DOMAIN / 'data' / icon_name).is_file():
    # Use local user path
    DIR_PREFIX = path_xdg_data_home / APP_DOMAIN
    DIR_LOCALE = path_xdg_data_home / 'locale'
    DIR_DOCS = path_xdg_data_home / 'doc' / APP_DOMAIN
elif (pathlib.Path(__file__).parent.parent / 'share' / APP_DOMAIN / 'data' /
      icon_name).is_file():
    # Use local user path in the local Python directory
    DIR_PREFIX = pathlib.Path(__file__).parent.parent / 'share' / APP_DOMAIN
    DIR_LOCALE = DIR_PREFIX.parent / 'locale'
    DIR_DOCS = DIR_PREFIX.parent / 'doc' / APP_DOMAIN
else:
    # Use system path
    path_prefix = pathlib.Path(sys.prefix)
    DIR_PREFIX = path_prefix / 'share' / APP_DOMAIN
    DIR_LOCALE = path_prefix / 'share' / 'locale'
    DIR_DOCS = path_prefix / 'share' / 'doc' / APP_DOMAIN
# Set the paths for the folders
DIR_DATA = DIR_PREFIX / 'data'
DIR_ICONS = DIR_DATA / 'icons'
DIR_UI = DIR_PREFIX / 'ui'
try:
    # In read-only environments, the settings folder cannot be created
    # (e.g. in a Debian pbuilder fakeroot)
    DIR_SETTINGS = pathlib.Path(BaseDirectory.save_config_path(APP_DOMAIN))
except PermissionError:
    # Get the settings path without actually creating it
    DIR_SETTINGS = pathlib.Path(BaseDirectory.xdg_config_home) / APP_DOMAIN
# Set the paths for the data files
FILE_ICON = DIR_DATA / icon_name
FILE_CONTRIBUTORS = DIR_DOCS / 'contributors'
FILE_TRANSLATORS = DIR_DOCS / 'translators'
FILE_LICENSE = DIR_DOCS / 'license'
FILE_RESOURCES = DIR_DOCS / 'resources'
# Set the paths for configuration files
FILE_SETTINGS = DIR_SETTINGS / 'settings.conf'
