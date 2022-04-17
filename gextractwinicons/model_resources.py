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
import logging
import os.path

from gi.repository import GdkPixbuf
from gi.repository import GLib


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

    def add_resource(self, parent, sType, name, language, width, height, depth,
                     path):
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
        except GLib.GError as error:
            # Empty image for invalid resources
            logging.error(f'Unable to get image for "{path}"')
            logging.error(str(error))
            pixbuf = None
        return self.model.append(parent, [True, sType, name, language,
                                          width, height, depth,
                                          os.path.getsize(path),
                                          pixbuf,
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
