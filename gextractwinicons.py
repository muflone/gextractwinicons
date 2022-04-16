#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##
#     Project: gExtractWinIcons
# Description: Extract cursors and icons from MS Windows compatible resource files.
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
