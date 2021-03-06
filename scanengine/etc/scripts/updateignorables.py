# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 nexB Inc. and others. All rights reserved.
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
from __future__ import unicode_literals
from __future__ import print_function


import click
click.disable_unicode_literals_warning = True

from licensedcode import cache
from licensedcode import models


"""
Update licenses and rules with ignorable copyrights, URLs and emails.
"""


def refresh_ignorables(licensishes):
    for i, lic in enumerate(sorted(licensishes)):
        print(i, end=' ')
        lic = models.update_ignorables(lic, verbose=True)
        lic.dump()


class _Nothing(object):
    pass



@click.command()
@click.argument('path',
    nargs=-1,
    type=click.Path(exists=False, allow_dash=False),
    metavar='PATH')


@click.help_option('-h', '--help')
def cli(path=(), update=True):
    """
    Update licenses and rules with ignorable copyrights, holders, authors URLs
    and emails.
    """
    licensish = list(cache.get_licenses_db().values()) + list(models.load_rules())

    if path:
        licensish = [l for l in licensish
            if l.text_file.endswith(path) or l.data_file.endswith(path)]
    refresh_ignorables(licensish)


if __name__ == '__main__':
    cli()
