#
# Copyright (c) nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scanengine-toolkit/
# The ScanEngine software is licensed under the Apache License version 2.0.
# Data generated with ScanEngine require an acknowledgment.
# ScanEngine is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanEngine or any ScanEngine
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanEngine and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanEngine should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanEngine is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scanengine-toolkit/ for support and download.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import errno
import os
from os.path import abspath
from os.path import dirname
from os.path import expanduser
from os.path import join
from os.path import exists
import tempfile

"""
Core configuration globals.

Note: this module MUST import ONLY from the standard library.
"""

# this exception is not available on POSIX
try:
    WindowsError  # NOQA
except NameError:
    class WindowsError(Exception):
        pass

def _create_dir(location):
    """
    Create directory and all sub-directories recursively at `location`.
    Raise Exceptions if it fails to create the directory.
    NOTE: this is essentailly a copy of commoncode.fileutils.create_dir()
    """

    if exists(location):
        if not os.path.isdir(location):
            err = ('Cannot create directory: existing file '
                   'in the way ''%(location)s.')
            raise OSError(err % locals())
        return

    # may fail on win if the path is too long
    # FIXME: consider using UNC ?\\ paths
    try:
        os.makedirs(location)

    # avoid multi-process TOCTOU conditions when creating dirs
    # the directory may have been created since the exist check
    except WindowsError as e:
        # [Error 183] Cannot create a file when that file already exists
        if e and e.winerror == 183:
            if not os.path.isdir(location):
                raise
        else:
            raise
    except (IOError, OSError) as o:
        if o.errno == errno.EEXIST:
            if not os.path.isdir(location):
                raise
        else:
            raise

################################################################################
# INVARIABLE INSTALLATION-SPECIFIC, BUILT-IN LOCATIONS AND FLAGS
################################################################################
# these are guaranteed to be there and are entirely based on and relative to the
# current installation location. This is where the source code and static data
# lives.


from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution('scanengine-toolkit').version
except DistributionNotFound:
    # package is not installed ??
    __version__ = '3.2.3'

system_temp_dir = tempfile.gettempdir()
scanengine_src_dir = dirname(__file__)
scanengine_root_dir = dirname(scanengine_src_dir)

################################################################################
# USAGE MODE FLAGS
################################################################################

# tag file or env var to determined if we are in dev mode
SCANENGINE_DEV_MODE = (
    os.getenv('SCANENGINE_DEV_MODE')
    or exists(join(scanengine_root_dir, 'SCANENGINE_DEV_MODE'))
)

################################################################################
# USAGE MODE-, INSTALLATION- and IMPORT- and RUN-SPECIFIC DIRECTORIES
################################################################################
# These vary based on the usage mode: dev or not and based on environamnet
# variables

# - scanengine_cache_dir: for long-lived caches which are installation-specific:
# this is for cached data which are infrequently written to and mostly readed,
# such as the license index cache. The same location is used across runs of
# a given version of ScanEngine
"""
We set the path to an existing directory where ScanEngine can cache files
available across runs from the value of the `SCANENGINE_CACHE` environment
variable. If `SCANENGINE_CACHE` is not set, a default sub-directory in the user
home directory is used instead.
"""
if SCANENGINE_DEV_MODE:
    # in dev mode the cache and temp files are stored execlusively under the
    # scanengine_root_dir
    scanengine_cache_dir = join(scanengine_root_dir, '.cache')
else:
    # In other usage modes (as a CLI or as a library, regardless of how
    # installed) we use sensible defaults in the user home directory.
    # These are version specific

    # WARNING: do not change this code without changing
    # commoncode.fileutils.get_temp_dir too

    user_home = abspath(expanduser('~'))
    __env_cache_dir = os.getenv('SCANENGINE_CACHE')
    scanengine_cache_dir = (__env_cache_dir
        or join(user_home, '.cache', 'scanengine-tk', __version__))

_create_dir(scanengine_cache_dir)


# - scanengine_temp_dir: for short-lived temporary files which are import- or run-
# specific that may live for the duration of a function call or for the duration
# of a whole scanengine run, such as any temp file and the per-run scan results
# cache. A new unique location is used for each run of ScanEngine (e.g. for the
# lifetime of the Python interpreter process)

"""
We set the path to an existing directory where ScanEngine can create temporary
files from the value of the `SCANENGINE_TMP` environment variable if available. If
`SCANENGINE_TMP` is not set, a default sub-directory in the system temp directory
is used instead. Each scan run creates its own tempfile subdirectory.
"""
__scanengine_temp_base_dir = os.getenv('SCANENGINE_TEMP')

if not __scanengine_temp_base_dir:
    if SCANENGINE_DEV_MODE:
        __scanengine_temp_base_dir = join(scanengine_root_dir, 'tmp')
    else:
        __scanengine_temp_base_dir = system_temp_dir

_create_dir(__scanengine_temp_base_dir)
_prefix = 'scanengine-tk-' + __version__ + '-'
scanengine_temp_dir = tempfile.mkdtemp(prefix=_prefix, dir=__scanengine_temp_base_dir)
