# gExtractWinIcons

[![Travis CI Build Status](https://img.shields.io/travis/com/muflone/gextractwinicons/master.svg)](https://www.travis-ci.com/github/muflone/gextractwinicons)
[![CircleCI Build Status](https://img.shields.io/circleci/project/github/muflone/gextractwinicons/master.svg)](https://circleci.com/gh/muflone/gextractwinicons)

**Description:** Extract cursors and icons from MS Windows resource files

**Copyright:** 2009-2022 Fabio Castelli (Muflone) <muflone@muflone.com>

**License:** GPL-3+

**Source code:** https://github.com/muflone/gextractwinicons/

**Documentation:** https://www.muflone.com/gextractwinicons/

**Translations:** https://explore.transifex.com/muflone/gextractwinicons/

# Description

From the *gExtractWinIcons* main window you select an MS Windows resources file
(like an exe, dll, cpl, ocx and so on) and you will list its contained resources
like cursors, icons and you can extract them, including exporting the icons in
PNG format.

![Main window](https://www.muflone.com/resources/gextractwinicons/archive/latest/english/main.png)

# System Requirements

* Python >= 3.6 (developed and tested for Python 3.9 and 3.10)
* XDG library for Python 3 ( https://pypi.org/project/pyxdg/ )
* GTK+ 3.0 libraries for Python 3
* GObject libraries for Python 3 ( https://pypi.org/project/PyGObject/ )
* IcoUtils package (wrestool and icotool commands)

# Installation

A distutils installation script is available to install from the sources.

To install in your system please use:

    cd /path/to/folder
    python3 setup.py install

To install the files in another path instead of the standard /usr prefix use:

    cd /path/to/folder
    python3 setup.py install --root NEW_PATH

# Usage

If the application is not installed please use:

    cd /path/to/folder
    python3 gextractwinicons.py

If the application was installed simply use the gextractwinicons command.
