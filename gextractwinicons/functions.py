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

from gettext import gettext as _

def readlines(filename, empty_lines = False):
  result = []
  with open(filename) as f:
    for line in f.readlines():
      line = line.strip()
      if line or empty_lines:
        result.append(line)
    f.close()
  return result

__all__ = [
  'readlines',
  '_'
]
