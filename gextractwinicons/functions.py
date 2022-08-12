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

from gi.repository import Gtk

from gextractwinicons.constants import DIR_UI


def bin_string_ascii(text: bytes) -> str:
    """Convert a binary string to string using ASCII codec"""
    return text.decode('ascii')


def bin_string_utf8(text: bytes) -> str:
    """Convert a binary string to string using UTF-8 codec"""
    return text.decode('utf-8')


def get_ui_file(filename):
    """Return the full path of a Glade/UI file"""
    return str(DIR_UI / filename)


def process_events():
    """Process every pending GTK+ event"""
    while Gtk.events_pending():
        Gtk.main_iteration()


def readlines(filename, empty_lines=False):
    result = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if line or empty_lines:
                result.append(line)
        f.close()
    return result
