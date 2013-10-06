#!/bin/bash
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
