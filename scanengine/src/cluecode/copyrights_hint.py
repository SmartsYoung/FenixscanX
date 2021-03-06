# -*- coding: utf-8 -*-
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

from datetime import datetime
import re

# A regex to match a string that may contain a copyright year.
# This is a year between 1960 and today prefixed and suffixed with
# either a white-space or some punctuation.

all_years = tuple(str(year) for year in range(1960, datetime.today().year))
years = r'[\(\.,\-\)\s]+(' + '|'.join(all_years) + r')([\(\.,\-\)\s]+|$)'

years = re.compile(years).findall

# Various copyright/copyleft signs tm, r etc: http://en.wikipedia.org/wiki/Copyright_symbol
# © U+00A9 COPYRIGHT SIGN
#  decimal: 169
#  HTML: &#169;
#  UTF-8: 0xC2 0xA9
#  block: Latin-1 Supplement
#  U+00A9 (169)
# visually similar: Ⓒ ⓒ
# 🄯 COPYLEFT SYMBOL
#  U+1F12F
# ℗ Sound recording copyright
#  HTML &#8471;
#  U+2117
# ® registered trademark
#  U+00AE (174)
# 🅪 Marque de commerce
#  U+1F16A
# ™ U+2122 TRADE MARK SIGN
#  decimal: 8482
#  HTML: &#8482;
#  UTF-8: 0xE2 0x84 0xA2
#  block: Letterlike Symbols
#  decomposition: <super> U+0054 U+004D
# Ⓜ  mask work


statement_markers = (
    u'©',
    u'(c)',
    u'&#169',
    u'&#xa9',
    u'00a9',
    u'\251',
    u'copyr',
    u'copyl',
    u'copr',
    u'right',
    u'reserv',
    u'auth',
    u'devel',
    u'<s>',
    u'</s>',
    u'<s/>',
    u'by ',  # note the trailing space
)
'''
HTML Entity (decimal)     &#169;
HTML Entity (hex)     &#xa9;
HTML Entity (named)     &copy;
How to type in Microsoft Windows     Alt +00A9
Alt 0169
UTF-8 (hex)     0xC2 0xA9 (c2a9)
UTF-8 (binary)     11000010:10101001
UTF-16 (hex)     0x00A9 (00a9)
UTF-16 (decimal)     169
UTF-32 (hex)     0x000000A9 (00a9)
UTF-32 (decimal)     169
C/C++/Java source code     "\u00A9"
Python source code     u"\u00A9"
'''

end_of_statement = (
    u'rights reserve',
    u'right reserve',
    u'rights reserved',
    u'right reserved',
    u'right reserved.',
)

# others stuffs
'''
&reg;
&trade;
trad
regi
hawlfraint
AB
AG
AS
auth
co
code
commit
common
comp
contrib
copyl
copyr
Copr
corp
devel
found
GB
gmbh
grou
holder
inc
inria
Lab
left
llc
ltd
llp
maint
micro
modi
compan
forum
oth
pack
perm
proj
research
sa
team
tech
tm
univ
upstream
write
'''.split()
