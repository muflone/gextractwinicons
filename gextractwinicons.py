#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##
#     Project: gExtractWinIcons
# Description: Extract cursors and icons from MS Windows compatible resource files.
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
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

import gettext
import locale
from gextractwinicons.settings import Settings
from gextractwinicons.app import Application
from gextractwinicons.constants import *

if __name__ == '__main__':
  # Load domain for translation
  for module in (gettext, locale):
    module.bindtextdomain(DOMAIN_NAME, DIR_LOCALE)
    module.textdomain(DOMAIN_NAME)

  # Load the settings from the configuration file
  settings = Settings()
  settings.load()

  # Start the application
  app = Application(settings)
  app.run(None)
