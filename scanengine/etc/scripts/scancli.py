#
# Copyright (c) 2019 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scanengine-toolkit/
# The ScanEngine software is licensed under the Apache License version 2.0.
# ScanEngine is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import OrderedDict
import json
from os.path import abspath
from os.path import dirname
from os.path import join
from os.path import normpath

import execnet

import scanserv

"""
This is a module designed to be called from Python 2 or 3 and is the client
side. See scanserv for the back server module that runs on Python 2 and runs
effectively scanengine.
"""


def scan(locations, deserialize=False, scanengine_root_dir=None):
    """
    Scan the list of paths at `location` and return the results as an iterable
    of JSON strings. If `deserialize` is True the iterable contains a python data
    instead.
    Each location is scanned independently.
    """
    if not scanengine_root_dir:
        scanengine_root_dir = abspath(normpath(__file__))
        scanengine_root_dir = dirname(dirname(dirname(scanengine_root_dir)))
    python2 = join(scanengine_root_dir, 'bin', 'python')
    spec = 'popen//python={python2}'.format(**locals())
    gateway = execnet.makegateway(spec)  # NOQA
    channel = gateway.remote_exec(scanserv)

    for location in locations:
        # build a mapping of options to use for this scan
        scan_kwargs = dict(
            location=location,
            license=True,
            license_text=True,
            copyright=True,
            info=True,
            processes=0,
        )

        channel.send(scan_kwargs)  # execute func-call remotely
        results = channel.receive()
        if deserialize:
            results = json.loads(results, object_pairs_hook=OrderedDict)
        yield results


if __name__ == '__main__':
    import sys  # NOQA
    args = sys.argv[1:]
    for s in scan(args):
        print(s)
