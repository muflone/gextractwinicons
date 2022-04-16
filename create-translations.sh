#!/bin/bash
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
