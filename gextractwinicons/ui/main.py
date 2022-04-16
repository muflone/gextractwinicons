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
import shutil

from gi.repository import Gtk

from gextractwinicons.ui.about import UIAbout
from gextractwinicons.constants import (APP_NAME,
                                        FILE_ICON,
                                        FILE_SETTINGS,
                                        RESOURCE_TYPE_GROUP_CURSOR,
                                        RESOURCE_TYPE_GROUP_ICON)
from gextractwinicons.extractor import Extractor
from gextractwinicons.functions import _
from gextractwinicons.model_resources import ModelResources
from gextractwinicons.settings import Settings
from gextractwinicons.ui.base import UIBase

SECTION_WINDOW_NAME = 'main window'


class UIMain(UIBase):
    def __init__(self, application, options):
        super().__init__(filename='main.ui')
        self.application = application
        self.options = options
        self.settings = Settings(FILE_SETTINGS, True)
        self.load_ui()
        self.settings.restore_window_position(window=self.ui.window,
                                              section=SECTION_WINDOW_NAME)
        self.is_refreshing = False
        # Load the others dialogs
        self.extractor = Extractor(self.settings)
        # Set initial resources file
        if self.options.filename:
            self.ui.btnFilePath.select_filename(self.options.filename)
            # Enable the refresh button if the filename was specified
            self.ui.btnRefresh.set_sensitive(True)
        # Set initial destination folder
        if self.options.destination:
            self.ui.btnDestination.set_filename(
                self.options.destination)
        else:
            self.ui.btnDestination.set_filename(os.path.expanduser('~'))
        # Save the resources totals
        self.total_resources = 0
        self.total_images = 0
        self.total_selected = 0

    def run(self):
        "Show the UI"
        self.ui.window.show_all()
        # Automatically refresh if the refresh setting was passed
        if self.options.refresh:
            self.on_btnFilePath_file_set(self.ui.btnFilePath)

    def load_ui(self):
        "Load the interface UI"
        # Obtain widget references
        self.model = ModelResources(self.ui.modelResources,
                                    self.settings)
        fileFilterMS = self.ui.fileFilterMS
        fileFilterAll = self.ui.fileFilterAll
        # Set various properties
        self.ui.window.set_title(APP_NAME)
        self.ui.window.set_icon_from_file(str(FILE_ICON))
        self.ui.window.set_application(self.application)
        # Add the filters for file selection button
        fileFilterMS.set_name(_('MS Windows compatible files'))
        self.ui.btnFilePath.add_filter(fileFilterMS)
        fileFilterAll.set_name(_('All files'))
        self.ui.btnFilePath.add_filter(fileFilterAll)
        self.ui.btnFilePath.set_filter(fileFilterMS)
        # Connect signals from the UI file to the functions with the same name
        self.ui.connect_signals(self)

    def update_totals(self):
        "Update totals on the label"
        self.ui.lblTotals.set_label(
            _('%d resources found (%d resources selected)') % (
                self.total_resources + self.total_images, self.total_selected))

    def on_window_delete_event(self, widget, event):
        "Close the application"
        self.extractor.destroy()
        self.settings.save_window_position(self.ui.window, SECTION_WINDOW_NAME)
        self.settings.save()
        self.ui.window.destroy()
        self.application.quit()

    def on_btnAbout_clicked(self, widget):
        """Show the about dialog"""
        about = UIAbout(parent=self.ui.window,
                        settings=self.settings,
                        options=self.options)
        about.show()
        about.destroy()

    def on_cellSelect_toggled(self, renderer, path):
        "Select and deselect an item"
        status = self.model.get_selected(path)
        self.model.set_selected(path, not status)
        # Add or subtract 1 from the total selected items count
        self.total_selected += status and -1 or 1
        self.update_totals()

    def on_btnFilePath_file_set(self, widget):
        "Activates or deactivates Refresh button if a file was set"
        if self.ui.btnFilePath.get_filename():
            self.ui.btnRefresh.set_property(
                'sensitive',
                bool(self.ui.btnFilePath.get_filename()))
            self.ui.btnRefresh.clicked()

    def on_btnRefresh_clicked(self, widget):
        "Extract the cursors and icons from the chosen filename"
        # Hide save button and show the ProgressBar
        if self.is_refreshing:
            logging.debug('Running extraction cancelled')
            self.is_refreshing = False
            return
        # Hide controls during the extraction
        self.ui.btnRefresh.set_label('gtk-stop')
        self.ui.btnFilePath.set_sensitive(False)
        self.ui.btnSelectAll.set_sensitive(False)
        self.ui.btnDeselectAll.set_sensitive(False)
        self.ui.btnSelectPNG.set_sensitive(False)
        self.ui.btnSaveResources.set_sensitive(False)
        logging.debug('Extraction started')
        self.is_refreshing = True
        self.ui.btnSaveResources.hide()
        self.ui.progLoading.set_fraction(0.0)
        self.ui.progLoading.show()
        if not self.options.nofreeze:
            # Freeze updates and disconnect model to load faster
            self.ui.tvwResources.freeze_child_notify()
            self.ui.tvwResources.set_model(None)
        # Clear the extractor directory
        self.extractor.clear()
        # Clear the previous items from the model
        self.model.clear()
        self.total_resources = 0
        self.total_images = 0
        self.total_selected = 0
        # List all the resources from the chosen filename
        all_resources = self.extractor.list(self.ui.btnFilePath.get_filename())
        resource_index = 0
        for resource in all_resources:
            # Cancel running extraction
            if not self.is_refreshing:
                break
            # Only cursors and icon groups are well supported by wrestool
            if resource['--type'] in (
                    RESOURCE_TYPE_GROUP_CURSOR, RESOURCE_TYPE_GROUP_ICON):
                logging.debug(f'Resource found: {resource}')
                # Extract the resource from the chosen filename
                resource_filename = self.extractor.extract(
                    self.ui.btnFilePath.get_filename(), resource)
                if resource_filename:
                    # Add resource to the tree and save iter to append children
                    iter_resource = self.model.add_resource(
                        None,
                        resource['--type'] == RESOURCE_TYPE_GROUP_CURSOR and _(
                            'cursors') or _('icons'),
                        resource['--name'],
                        resource['--language'],
                        None,
                        None,
                        None,
                        resource_filename
                    )
                    self.total_resources += 1
                    self.total_selected += 1
                    # Extract all the images from the resource
                    for image in self.extractor.extract_images(
                            resource_filename):
                        # Cancel running extraction
                        if not self.is_refreshing:
                            break
                        if '--icon' in image:
                            image['--type'] = _('icon')
                        elif '--cursor' in image:
                            image['--type'] = _('cursor')
                        else:
                            image['--type'] = None
                        # Add children images to the resource in the treeview
                        self.model.add_resource(
                            iter_resource,
                            image['--type'],
                            image['--index'],
                            '',
                            image['--width'],
                            image['--height'],
                            image['--bit-depth'],
                            image['path']
                        )
                        self.total_images += 1
                        self.total_selected += 1
                        # Let the interface to continue its main loop
                        while Gtk.events_pending():
                            Gtk.main_iteration()
            # Update the ProgressBar
            resource_index += 1
            self.ui.progLoading.set_fraction(
                float(resource_index) / len(all_resources))
        # End of resources loading
        self.ui.progLoading.hide()
        self.ui.btnFilePath.set_sensitive(True)
        self.ui.btnSelectAll.set_sensitive(True)
        self.ui.btnDeselectAll.set_sensitive(True)
        self.ui.btnSelectPNG.set_sensitive(True)
        self.ui.btnSaveResources.set_sensitive(True)
        self.ui.btnSaveResources.show()
        self.ui.btnRefresh.set_label('gtk-refresh')
        if not self.options.nofreeze:
            # Unfreeze the treeview from refresh
            self.ui.tvwResources.set_model(self.model.get_model())
            self.ui.tvwResources.thaw_child_notify()
        self.ui.tvwResources.expand_all()
        status = 'completed' if self.is_refreshing else 'canceled'
        logging.info(f'Extraction {status} '
                     f'({self.total_resources} resources found, '
                     f'{self.total_images} images found)')
        self.is_refreshing = False
        self.update_totals()

    def on_btnSaveResources_clicked(self, widget):
        "Save the selected resources"
        destination_path = self.ui.btnDestination.get_filename()
        saved_count = 0
        # Iter the first level
        for iter in self.model.get_model():
            if self.model.get_selected(iter.path):
                # Copy ico/cur file
                shutil.copy(self.model.get_file_path(iter.path),
                            destination_path)
                saved_count += 1
            # Iter the children
            for iter in iter.iterchildren():
                if self.model.get_selected(iter.path):
                    # Copy PNG image
                    shutil.copy(self.model.get_file_path(iter.path),
                                destination_path)
                    saved_count += 1
        logging.info(f'{saved_count} resources were saved '
                     f'to {destination_path}')
        # Show the completion dialog
        dialog = Gtk.MessageDialog(
            parent=self.ui.window,
            flags=Gtk.DialogFlags.MODAL,
            type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            message_format=_('Extraction completed.')
        )
        dialog.set_title(APP_NAME)
        dialog.set_icon_from_file(str(FILE_ICON))
        dialog.run()
        dialog.destroy()

    def on_btnSelect_clicked(self, widget):
        "Deselect or select all the resources or only the images"
        self.total_selected = 0
        for iter in self.model.get_model():
            # Iter the resources
            if widget is self.ui.btnSelectAll:
                self.model.set_selected(iter.path, True)
                self.total_selected += 1
            elif (widget is self.ui.btnDeselectAll or
                  widget is self.ui.btnSelectPNG):
                self.model.set_selected(iter.path, False)
            # Iter the images
            for iter in iter.iterchildren():
                if (widget is self.ui.btnSelectAll) or (
                        widget is self.ui.btnSelectPNG):
                    self.model.set_selected(iter.path, True)
                    self.total_selected += 1
                elif widget is self.ui.btnDeselectAll:
                    self.model.set_selected(iter.path, False)
        self.update_totals()
