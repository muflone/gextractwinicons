#!/bin/bash
intltool-extract --type=gettext/glade ../data/gextractwinicons.glade
if [ -f gextractwinicons.pot ]
then
  rm gextractwinicons.pot
fi
xgettext --language=Python --keyword=_ --keyword=N_ --output gextractwinicons.pot ../data/*.glade.h ../gextractwinicons
rm ../data/*.glade.h
