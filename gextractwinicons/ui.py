##
#     Project: gExtractWinIcons
# Description: Extract cursors and icons from MS Windows compatible resource files.
#      Author: Fabio Castelli (Muflone) <webreg@vbsimple.net>
#   Copyright: 2009-2013 Fabio Castelli
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

from gi.repository import Gtk
from gi.repository import Gio
from gextractwinicons.constants import *
from gextractwinicons.functions import *
from gextractwinicons.settings import Settings
from gextractwinicons.model_resources import ModelResources
from gextractwinicons.about import AboutWindow
from gextractwinicons.extractor import Extractor

class MainWindow(object):
  def __init__(self, application, settings):
    self.application = application
    self.settings = settings
    self.is_refreshing = False
    self.loadUI()
    # Restore the saved size and position
    if self.settings.get_value('width', 0) and self.settings.get_value('height', 0):
      self.winMain.set_default_size(
        self.settings.get_value('width', -1),
        self.settings.get_value('height', -1))
    if self.settings.get_value('left', 0) and self.settings.get_value('top', 0):
      self.winMain.move(
        self.settings.get_value('left', 0),
        self.settings.get_value('top', 0))
    # Load the others dialogs
    self.about = AboutWindow(self.winMain, False)
    self.extractor = Extractor(self.settings)
    # Set initial resources file
    if self.settings.options.filename:
      self.btnFilePath.select_filename(self.settings.options.filename)
      # Enable the refresh button if the filename was specified
      self.btnRefresh.set_sensitive(True)
    # Set initial destination folder
    if self.settings.options.destination:
      self.btnDestination.set_filename(self.settings.options.destination)
    else:
      self.btnDestination.set_filename(os.path.expanduser('~'))
    # Save the resources totals
    self.total_resources = 0
    self.total_images = 0
    self.total_selected = 0

  def run(self):
    "Show the UI"
    self.winMain.show_all()
    # Automatically refresh if the refresh setting was passed
    if self.settings.options.refresh:
      self.on_btnFilePath_file_set(self.btnFilePath)

  def loadUI(self):
    "Load the interface UI"
    builder = Gtk.Builder()
    builder.add_from_file(FILE_UI_MAIN)
    # Obtain widget references
    self.winMain = builder.get_object("winMain")
    self.model = ModelResources(builder.get_object('modelResources'), self.settings)
    self.tvwResources = builder.get_object('tvwResources')
    self.btnFilePath = builder.get_object('btnFilePath')
    fileFilterMS = builder.get_object('fileFilterMS')
    fileFilterAll = builder.get_object('fileFilterAll')
    self.btnDestination = builder.get_object('btnDestination')
    self.btnRefresh = builder.get_object('btnRefresh')
    self.lblTotals = builder.get_object('lblTotals')
    self.progLoading = builder.get_object('progLoading')
    self.btnSelectAll = builder.get_object('btnSelectAll')
    self.btnDeselectAll = builder.get_object('btnDeselectAll')
    self.btnSelectPNG = builder.get_object('btnSelectPNG')
    self.btnSaveResources = builder.get_object('btnSaveResources')
    # Set various properties
    self.winMain.set_title(APP_NAME)
    self.winMain.set_icon_from_file(FILE_ICON)
    self.winMain.set_application(self.application)
    # Add the filters for file selection button
    fileFilterMS.set_name(_('MS Windows compatible files'))
    self.btnFilePath.add_filter(fileFilterMS)
    fileFilterAll.set_name(_('All files'))
    self.btnFilePath.add_filter(fileFilterAll)
    self.btnFilePath.set_filter(fileFilterMS)
    # Connect signals from the glade file to the functions with the same name
    builder.connect_signals(self)

  def update_totals(self):
    "Update totals on the label"
    self.lblTotals.set_label(_('%d resources found (%d resources selected)') % (
      self.total_resources + self.total_images, self.total_selected))

  def on_winMain_delete_event(self, widget, event):
    "Close the application"
    self.extractor.destroy()
    self.about.destroy()
    self.settings.set_sizes(self.winMain)
    self.settings.save()
    self.winMain.destroy()
    self.application.quit()

  def on_btnAbout_clicked(self, widget):
    "Show the about dialog"
    self.about.show()

  def on_cellSelect_toggled(self, renderer, iter):
    "Select and deselect an item"
    status = self.model.get_selected(iter)
    self.model.set_selected(iter, not status)
    # Add or subtract 1 from the total selected items count
    self.total_selected += status and -1 or 1
    self.update_totals()

  def on_btnFilePath_file_set(self, widget):
    "Activates or deactivates Refresh button if a file was set"
    if self.btnFilePath.get_filename():
      self.btnRefresh.set_property('sensitive', 
        bool(self.btnFilePath.get_filename()))
      self.btnRefresh.clicked()

  def on_btnRefresh_clicked(self, widget):
    "Extract the cursors and icons from the chosen filename"
    # Hide save button and show the ProgressBar
    if self.is_refreshing:
      self.settings.logText('Running extraction cancelled', VERBOSE_LEVEL_MAX)
      self.is_refreshing = False
      return
    # Hide controls during the extraction
    self.btnRefresh.set_label('gtk-stop')
    self.btnFilePath.set_sensitive(False)
    self.btnSelectAll.set_sensitive(False)
    self.btnDeselectAll.set_sensitive(False)
    self.btnSelectPNG.set_sensitive(False)
    self.btnSaveResources.set_sensitive(False)
    self.settings.logText('Extraction started', VERBOSE_LEVEL_MAX)
    self.is_refreshing = True
    self.btnSaveResources.hide()
    self.progLoading.set_fraction(0.0)
    self.progLoading.show()
    if not self.settings.options.nofreeze:
      # Freeze updates and disconnect model to load faster
      self.tvwResources.freeze_child_notify()
      self.tvwResources.set_model(None)
    # Clear the extractor directory
    self.extractor.clear()
    # Clear the previous items from the model
    self.model.clear()
    self.total_resources = 0
    self.total_images = 0
    self.total_selected = 0
    # List all the resources from the chosen filename
    all_resources = self.extractor.list(self.btnFilePath.get_filename())
    resource_index = 0
    for resource in all_resources:
      # Cancel running extraction
      if not self.is_refreshing:
        break
      # Only cursors and icon groups are well supported by wrestool
      if resource['--type'] in (
        RESOURCE_TYPE_GROUP_CURSOR, RESOURCE_TYPE_GROUP_ICON):
        self.settings.logText("Resource found:%s" % resource, VERBOSE_LEVEL_MAX)
        # Extract the resource from the chosen filename
        resource_filename = self.extractor.extract(
          self.btnFilePath.get_filename(), resource)
        if resource_filename:
          # Add the resource to the tree and save the iter to append children
          iter_resource = self.model.add_resource(
            None,
            resource['--type'] == RESOURCE_TYPE_GROUP_CURSOR and _('cursors') or _('icons'),
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
          for image in self.extractor.extract_images(resource_filename):
            # Cancel running extraction
            if not self.is_refreshing:
              break
            if image.has_key('--icon'):
              image['--type'] = _('icon')
            elif image.has_key('--cursor'):
              image['--type'] = _('cursor')
            else:
              image['--type'] = None
            # Add the children images to the resource in the treeview
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
      self.progLoading.set_fraction(float(resource_index) / len(all_resources))
    # End of resources loading
    self.progLoading.hide()
    self.btnFilePath.set_sensitive(True)
    self.btnSelectAll.set_sensitive(True)
    self.btnDeselectAll.set_sensitive(True)
    self.btnSelectPNG.set_sensitive(True)
    self.btnSaveResources.set_sensitive(True)
    self.btnSaveResources.show()
    self.btnRefresh.set_label('gtk-refresh')
    if not self.settings.options.nofreeze:
      # Unfreeze the treeview from refresh
      self.tvwResources.set_model(self.model.get_model())
      self.tvwResources.thaw_child_notify()
    self.tvwResources.expand_all()
    self.settings.logText(
      'Extraction %s (%d resources found, %d images found)' % (
        self.is_refreshing and 'completed' or 'canceled',
        self.total_resources,
        self.total_images
      ),
      VERBOSE_LEVEL_NORMAL)
    self.is_refreshing = False
    self.update_totals()

  def on_btnSaveResources_clicked(self, widget):
    pass

  def on_btnSelect_clicked(self, widget):
    "Deselect or select all the resources or only the images"
    self.total_selected = 0
    for iter in self.model.get_model():
      # Iter the resources
      if widget is self.btnSelectAll:
        self.model.set_selected(iter.path, True)
        self.total_selected += 1
      elif widget is self.btnDeselectAll or widget is self.btnSelectPNG:
        self.model.set_selected(iter.path, False)
      # Iter the images
      for iter in iter.iterchildren():
        if (widget is self.btnSelectAll) or (widget is self.btnSelectPNG):
          self.model.set_selected(iter.path, True)
          self.total_selected += 1
        elif widget is self.btnDeselectAll:
          self.model.set_selected(iter.path, False)
    self.update_totals()
