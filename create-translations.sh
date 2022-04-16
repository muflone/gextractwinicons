#!/bin/bash
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
LOCALEDIR="locale"
[ -d "$LOCALEDIR" ] && rm -rf "$LOCALEDIR"
mkdir "$LOCALEDIR"
for FILEPO in po/*.po;
do (
  FILEMO=$(basename "$FILEPO" .po)
  mkdir -p "$LOCALEDIR/$FILEMO/LC_MESSAGES"
  msgfmt --output-file="$LOCALEDIR/$FILEMO/LC_MESSAGES/gextractwinicons.mo" "$FILEPO"
)
done
