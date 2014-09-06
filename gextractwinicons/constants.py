##
#     Project: gExtractWinIcons
# Description: Extract cursors and icons from MS Windows compatible resource files.
#      Author: Fabio Castelli (Muflone) <webreg@vbsimple.net>
#   Copyright: 2009-2014 Fabio Castelli
#     License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

import sys
import os.path
from xdg import BaseDirectory

# Application constants
APP_NAME = 'gExtractWinIcons'
APP_VERSION = '0.4.1'
APP_DESCRIPTION = 'Extract cursors and icons from MS Windows compatible resource files.'
APP_ID = 'gextractwinicons.muflone.com'
APP_URL = 'http://url.muflone.com/gextractwinicons'
APP_AUTHOR = 'Fabio Castelli'
APP_AUTHOR_EMAIL = 'webreg@vbsimple.net'
APP_COPYRIGHT = 'Copyright 2009-2014 %s' % APP_AUTHOR
# Other constants
DOMAIN_NAME = 'gextractwinicons'
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
# If there's a file data/gextractwinicons.png then the shared data are searched
# in relative paths, else the standard paths are used
if os.path.isfile(os.path.join('data', 'gextractwinicons.png')):
  DIR_PREFIX = '.'
  DIR_LOCALE = os.path.join(DIR_PREFIX, 'locale')
  DIR_DOCS = os.path.join(DIR_PREFIX, 'doc')
else:
  DIR_PREFIX = os.path.join(sys.prefix, 'share', 'gextractwinicons')
  DIR_LOCALE = os.path.join(sys.prefix, 'share', 'locale')
  DIR_DOCS = os.path.join(sys.prefix, 'share', 'doc', 'gextractwinicons')
# Set the paths for the folders
DIR_DATA = os.path.join(DIR_PREFIX, 'data')
DIR_UI = os.path.join(DIR_PREFIX, 'ui')
DIR_SETTINGS = BaseDirectory.save_config_path(DOMAIN_NAME)
# Set the paths for the UI files
FILE_UI_MAIN = os.path.join(DIR_UI, 'main.glade')
FILE_UI_ABOUT = os.path.join(DIR_UI, 'about.glade')
FILE_UI_APPMENU = os.path.join(DIR_UI, 'appmenu.ui')
# Set the paths for the data files
FILE_ICON = os.path.join(DIR_DATA, 'gextractwinicons.png')
FILE_TRANSLATORS = os.path.join(DIR_DOCS, 'translators')
FILE_LICENSE = os.path.join(DIR_DOCS, 'license')
FILE_RESOURCES = os.path.join(DIR_DOCS, 'resources')
# Set the paths for configuration files
FILE_SETTINGS_NEW = os.path.join(DIR_SETTINGS, 'settings.conf')
