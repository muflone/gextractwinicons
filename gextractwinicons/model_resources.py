##
#     Project: gExtractWinIcons
# Description: Extract cursors and icons from MS Windows compatible resource files.
#      Author: Fabio Castelli (Muflone) <webreg@vbsimple.net>
#   Copyright: 2009-2013 Fabio Castelli
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

import os.path
from gi.repository import GdkPixbuf
from gextractwinicons.constants import *
from gextractwinicons.functions import *

class ModelResources(object):
  COL_SELECTED = 0
  COL_TYPE = 1
  COL_NAME = 2
  COL_LANGUAGE = 3
  COL_WIDTH = 4
  COL_HEIGHT = 5
  COL_DEPTH = 6
  COL_SIZE = 7
  COL_PREVIEW = 8
  COL_FILEPATH = 9
  def __init__(self, model, settings):
    self.model = model
    self.settings = settings

  def clear(self):
    "Clear the model"
    return self.model.clear()

  def add_resource(self, parent, sType, name, language, width, height, depth, path):
    return self.model.append(parent, [True, sType, name, language, 
      width, height, depth,
      os.path.getsize(path),
      GdkPixbuf.Pixbuf.new_from_file(path),
      path
    ])

  def get_selected(self, path):
    return self.model[path][self.__class__.COL_SELECTED]

  def set_selected(self, path, value):
    self.model[path][self.__class__.COL_SELECTED] = value

  def get_file_path(self, path):
    return self.model[path][self.__class__.COL_FILEPATH]

  def get_model(self):
    return self.model
