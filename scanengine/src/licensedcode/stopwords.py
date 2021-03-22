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
from __future__ import print_function
from __future__ import unicode_literals


"""
A set of common words that are ignored from matching such as HTML tags.
"""

STOPWORDS = frozenset({
# common XML character references as &quot;
    'quot',
    'apos',
    'lt',
    'gt',
    'amp',
    'nbsp',

# common html tags as <a href=https://link ...> dfsdfsdf</a>
    'a',
    'href',
    'p',
    'br',
    'div',
    'em',
    'span',
    'class',
    'pre',
    'ul',
    'ol',
    'li',
    'hr',
    'tr',
    'td',
    'th',
    'img',
    'alt',
    'src',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'blockquote',
    'body',
    #'id',
    'script',
    'rel',

# debian copyright files <s> tags
    's',

# comment line markers
    # batch files
    'rem',
    # autotools
    'dnl',

# doc book tags as <para>
    'ulink',
    'para',

# Some HTML punctuations and entities all as &emdash;
    'ge',
    'le',
    'emdash',  # rare and weird
    'mdash',
    'ndash',
    'bdquo',
    'ldquo',
    'ldquor',
    'lsaquo',
    'lsquo',
    'lsquor',
    'raquo',
    'rdquo',
    'rdquor',
    'rsaquo',
    'rsquo',
    'rsquor',
    'sbquo',
    'lpar',
    'rpar',
    'comma',
    'period',
    'colon',
    'semi',
    'tilde',
    'emsp',
    'ensp',
    'numsp',
    'puncsp',
    'thinsp',
    'hairsp',
    'bull',
    'bullet',
    # some xml char entities
    'x3c',
    'x3e',

    # seen in many CSS
    'lists',
    'side', 'nav',
    'height',
    'auto',
    'border',
    'padding',
    'width',

    # seen in Perl PODs
    'f',
    'head1',
    'head2',
    'head3',

    # seen in RTF markup
    # this may be a solution to https://github.com/nexB/scanengine-toolkit/issues/1548
    # 'par',

    # TODO: consider common english stop words (the of a ...)
    # 'the',
    # 'of',
    # 'a',

    # common in C literals
    'printf',

    # common in shell
    'echo',

})


# query breaks
# in Android generated NOTICE.html files
breaks = {
    '<pre class="license-text">',
    '</pre><!-- license-text -->',
    '-------------------------------------------------------------------',
    '==============================================================================',
}


# TODO: use me?
# translations of HTML entities to words or letters
{
    '&eacute': 'e',
    '&copy': '(c)',
}
