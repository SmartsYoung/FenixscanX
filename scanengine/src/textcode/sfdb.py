#
# Copyright (c) 2018 nexB Inc. and others. All rights reserved.
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
from __future__ import print_function
from __future__ import unicode_literals

"""
Specialized processing for Spline Font Database files from Fontforge
https://fontforge.github.io/en-US/documentation/developers/sfdformat/
"""


def get_text_lines(location):
    """
    Return a list of unicode text lines extracted from a spline font DB file at
    `location`.
    """
    interesting_lines = (
        b'Copyright:', b'LangName:',
        b'FontName:', b'FullName:',
        b'FamilyName:', b'Version:',
    )
    with open(location, 'rb') as sfdb_file:
        for line in sfdb_file:
            if line.startswith(interesting_lines):
                yield line
