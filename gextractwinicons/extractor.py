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

import logging
import os
import os.path
import subprocess
import tempfile

from gextractwinicons.constants import APP_NAME, RESOURCE_TYPE_GROUP_CURSOR
from gextractwinicons.functions import bin_string_utf8


class Extractor(object):
    def __init__(self, settings):
        # Create a temporary directory for the extracted icons
        self.settings = settings
        self.tempdir = tempfile.mkdtemp(prefix=f'{APP_NAME}-')
        logging.debug('The temporary files will be extracted '
                      f'under {self.tempdir}')

    def clear(self):
        for f in os.listdir(self.tempdir):
            os.remove(os.path.join(self.tempdir, f))

    def destroy(self):
        """Clear and delete the temporary directory"""
        self.clear()
        os.rmdir(self.tempdir)
        self.tempdir = None

    def list(self, filename):
        """Extract the resources list from the filename"""
        resources = []
        proc = subprocess.Popen(
            ['wrestool', '--list', filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if stderr:
            logging.debug('wrestool --list '
                          f'error: {bin_string_utf8(stderr).strip()}')
        # Remove weird characters
        stdout = stdout.decode('utf-8').replace('[', '')
        stdout = stdout.replace(']', '')
        for line in stdout.split('\n'):
            resource = {}
            for options in line.split():
                if '=' in options:
                    arg, value = options.split('=')
                    resource[arg] = value.replace('\'', '')
            # A resource was found
            if resource:
                if resource.get('--type', '0').isdigit():
                    resource['--type'] = int(resource['--type'])
                else:
                    resource['--type'] = 0
                resources.append(resource)
        return resources

    def extract(self, filename, resource):
        """Extract a resource to the temporary directory"""
        output_filename = os.path.join(
            self.tempdir, '%s_%d_%s_%s.%s' % (
                os.path.basename(filename),
                resource['--type'],
                resource['--name'],
                resource['--language'],
                ('cur'
                 if resource['--type'] == RESOURCE_TYPE_GROUP_CURSOR
                 else 'ico')
            ))
        proc = subprocess.Popen(
            [
                'wrestool',
                '--extract',
                '--type', str(resource['--type']),
                '--name', resource['--name'],
                '--language', resource['--language'],
                '--output', output_filename,
                filename
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if stderr:
            logging.debug('wrestool --extract '
                          f'error: {bin_string_utf8(stderr).strip()}')
        # Check if the resource was extracted successfully (cannot be sure)
        if os.path.isfile(output_filename):
            return output_filename

    def extract_images(self, filename):
        """Extract the images from a cursor or icon file"""
        images = []
        # Retrieve the images inside the cursor/icon file
        proc = subprocess.Popen(
            ['icotool', '--list', filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if stderr:
            logging.debug('icotool --list '
                          f'error: {bin_string_utf8(stderr).strip()}')

        # Split line in fields
        for line in stdout.decode('utf-8').split('\n'):
            resource = {}
            for options in line.split():
                if '=' in options:
                    arg, value = options.split('=')
                else:
                    arg = options
                    value = None
                resource[arg] = value
            # A resource was found
            if resource:
                # Determine the temporary output filename
                # like 'name_index_WxHxD.png'
                output_filename = os.path.join(
                    self.tempdir, '%s_%s_%sx%sx%s.png' % (
                        filename[:-4],
                        resource['--index'],
                        resource['--width'],
                        resource['--height'],
                        resource['--bit-depth']))
                # Extract the image from the resource into the file
                proc = subprocess.Popen(
                    [
                        'icotool',
                        '--extract',
                        '--index', resource['--index'],
                        '--width', resource['--width'],
                        '--height', resource['--height'],
                        '--bit-depth', resource['--bit-depth'],
                        '--output', output_filename,
                        filename
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()
                if stderr:
                    logging.debug('icotool --extract '
                                  f'error: {bin_string_utf8(stderr).strip()}')
                # Check if the image was extracted successfully
                if os.path.isfile(output_filename):
                    resource['path'] = output_filename
                    images.append(resource)
        return images
