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
from __future__ import division
from __future__ import print_function

from functools import partial
import textwrap


"""
Utility function to trace matched texts.
"""


def get_texts(match, width=80, margin=0):
    """
    Given a match and a query location of query string return a tuple of wrapped
    texts at `width` for:

    - the matched query text as a string.
    - the matched rule text as a string.

    If `width` is a number superior to zero, the texts are wrapped to width.
    """
    qtokens = match.matched_text(whole_lines=False).split()
    mqt = format_text(tokens=qtokens, width=width, margin=margin)

    itokens = matched_rule_tokens_str(match)
    mit = format_text(tokens=itokens, width=width, margin=margin)

    return mqt, mit


def format_text(tokens, width=80, margin=4):
    """
    Return a formatted text wrapped at `width` given an iterable of tokens.
    None tokens for unmatched positions are replaced with `no_match`.
    """
    noop = lambda x: [x]
    initial_indent = subsequent_indent = u' ' * margin
    wrapper = partial(textwrap.wrap,
        width=width,
        break_on_hyphens=False,
        initial_indent=initial_indent,
        subsequent_indent=subsequent_indent)
    wrap = width and wrapper or noop
    return u'\n'.join(wrap(u' '.join(tokens)))


def matched_rule_tokens_str(match):
    """
    Return an iterable of matched rule token strings given a match.
    Punctuation is removed, spaces are normalized (new line is replaced by a space),
    case is preserved.
    """
    for pos, token in enumerate(match.rule.tokens()):
        if match.ispan.start <= pos <= match.ispan.end:
            if pos in match.ispan:
                yield token
            else:
                yield '<%s>' % token
