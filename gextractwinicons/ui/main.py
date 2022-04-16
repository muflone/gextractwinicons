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

from gextractwinicons.constants import (APP_NAME,
                                        FILE_ICON,
                                        FILE_SETTINGS,
                                        RESOURCE_TYPE_GROUP_CURSOR,
                                        RESOURCE_TYPE_GROUP_ICON)
from gextractwinicons.extractor import Extractor
from gextractwinicons.functions import process_events, _
from gextractwinicons.model_resources import ModelResources
from gextractwinicons.settings import Settings
from gextractwinicons.ui.about import UIAbout
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
            self.ui.button_filename.select_filename(self.options.filename)
            # Enable the refresh button if the filename was specified
            self.ui.button_refresh.set_sensitive(True)
        # Set initial destination folder
        if self.options.destination:
            self.ui.button_destination.set_filename(
                self.options.destination)
        else:
            self.ui.button_destination.set_filename(os.path.expanduser('~'))
        # Save the resources totals
        self.total_resources = 0
        self.total_images = 0
        self.total_selected = 0

    def run(self):
        "Show the UI"
        self.ui.window.show_all()
        # Automatically refresh if the refresh setting was passed
        if self.options.refresh:
            self.on_button_filename_file_set(self.ui.button_filename)

    def load_ui(self):
        "Load the interface UI"
        # Obtain widget references
        self.model = ModelResources(model=self.ui.store_resources,
                                    settings=self.settings)
        # Initialize titles and tooltips
        self.set_titles()
        # Set various properties
        self.ui.window.set_title(APP_NAME)
        self.ui.window.set_icon_from_file(str(FILE_ICON))
        self.ui.window.set_application(self.application)
        # Add the filters for file selection button
        self.ui.file_filter_ms.set_name(_('MS Windows compatible files'))
        self.ui.button_filename.add_filter(self.ui.file_filter_ms)
        self.ui.file_filter_all.set_name(_('All files'))
        self.ui.button_filename.add_filter(self.ui.file_filter_all)
        self.ui.button_filename.set_filter(self.ui.file_filter_ms)
        # Connect signals from the UI file to the functions with the same name
        self.ui.connect_signals(self)

    def update_totals(self):
        "Update totals on the label"
        self.ui.label_totals.set_label(
            _('%d resources found (%d resources selected)') % (
                self.total_resources + self.total_images, self.total_selected))

    def on_window_delete_event(self, widget, event):
        "Close the application"
        """Close the application by closing the main window"""
        self.ui.action_quit.emit('activate')

    def on_action_quit_activate(self, widget):
        """Quit the application"""
        self.extractor.destroy()
        self.settings.save_window_position(self.ui.window, SECTION_WINDOW_NAME)
        self.settings.save()
        self.ui.window.destroy()
        self.application.quit()

    def on_action_about_activate(self, widget):
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

    def on_button_filename_file_set(self, widget):
        "Activates or deactivates Refresh button if a file was set"
        if self.ui.button_filename.get_filename():
            self.ui.button_refresh.set_property(
                'sensitive',
                bool(self.ui.button_filename.get_filename()))
            self.ui.button_refresh.clicked()

    def on_button_refresh_clicked(self, widget):
        "Extract the cursors and icons from the chosen filename"
        # Hide save button and show the ProgressBar
        if self.is_refreshing:
            logging.debug('Running extraction cancelled')
            self.is_refreshing = False
            return
        # Hide controls during the extraction
        self.ui.button_refresh.set_label('gtk-stop')
        self.ui.button_filename.set_sensitive(False)
        self.ui.button_select_all.set_sensitive(False)
        self.ui.button_deselect_all.set_sensitive(False)
        self.ui.button_select_png.set_sensitive(False)
        self.ui.button_save_resources.set_sensitive(False)
        logging.debug('Extraction started')
        self.is_refreshing = True
        self.ui.button_save_resources.hide()
        self.ui.progress_loader.set_fraction(0.0)
        self.ui.progress_loader.show()
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
        all_resources = self.extractor.list(
            filename=self.ui.button_filename.get_filename())
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
                    self.ui.button_filename.get_filename(), resource)
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
                        process_events()
            # Update the ProgressBar
            resource_index += 1
            self.ui.progress_loader.set_fraction(
                float(resource_index) / len(all_resources))
        # End of resources loading
        self.ui.progress_loader.hide()
        self.ui.button_filename.set_sensitive(True)
        self.ui.button_select_all.set_sensitive(True)
        self.ui.button_deselect_all.set_sensitive(True)
        self.ui.button_select_png.set_sensitive(True)
        self.ui.button_save_resources.set_sensitive(True)
        self.ui.button_save_resources.show()
        self.ui.button_refresh.set_label('gtk-refresh')
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

    def on_button_save_resources_clicked(self, widget):
        "Save the selected resources"
        destination_path = self.ui.button_destination.get_filename()
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

    def on_button_select_clicked(self, widget):
        "Deselect or select all the resources or only the images"
        self.total_selected = 0
        for iter in self.model.get_model():
            # Iter the resources
            if widget is self.ui.button_select_all:
                self.model.set_selected(iter.path, True)
                self.total_selected += 1
            elif (widget is self.ui.button_deselect_all or
                  widget is self.ui.button_select_png):
                self.model.set_selected(iter.path, False)
            # Iter the images
            for iter in iter.iterchildren():
                if (widget is self.ui.button_select_all) or (
                        widget is self.ui.button_select_png):
                    self.model.set_selected(iter.path, True)
                    self.total_selected += 1
                elif widget is self.ui.button_deselect_all:
                    self.model.set_selected(iter.path, False)
        self.update_totals()
