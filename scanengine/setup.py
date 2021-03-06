#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
import re
import sys

from setuptools import find_packages
from setuptools import setup

version = '0.0.1'

#### Small hack to force using a plain version number if the option
#### --plain-version is passed to setup.py

USE_DEFAULT_VERSION = False
try:
    sys.argv.remove('--use-default-version')
    USE_DEFAULT_VERSION = True
except ValueError:
    pass
####


_sys_v0 = sys.version_info[0]
py2 = _sys_v0 == 2
py3 = _sys_v0 == 3


def get_version(default=version, template='{tag}.{distance}.{commit}{dirty}',
                use_default=USE_DEFAULT_VERSION):
    """
    Return a version collected from git if possible or fall back to an
    hard-coded default version otherwise. If `use_default` is True,
    always use the default version.
    """
    if use_default:
        return default
    try:
        tag, distance, commit, dirty = get_git_version()
        if not distance and not dirty:
            # we are from a clean Git tag: use tag
            return tag

        distance = 'post{}'.format(distance)
        if dirty:
            time_stamp = get_time_stamp()
            dirty = '.dirty.' + get_time_stamp()
        else:
            dirty = ''

        return template.format(**locals())
    except:
        # no git data: use default version
        return default


def get_time_stamp():
    """
    Return a numeric UTC time stamp without microseconds.
    """
    from datetime import datetime
    return (datetime.isoformat(datetime.utcnow()).split('.')[0]
            .replace('T', '').replace(':', '').replace('-', ''))


def get_git_version():
    """
    Return version parts from Git or raise an exception.
    """
    from subprocess import check_output, STDOUT
    # this may fail with exceptions
    cmd = 'git', 'describe', '--tags', '--long', '--dirty',
    version = check_output(cmd, stderr=STDOUT).strip()
    dirty = version.endswith('-dirty')
    tag, distance, commit = version.split('-')[:3]
    # lower tag and strip V prefix in tags
    tag = tag.lower().lstrip('v ').strip()
    # strip leading g from git describe commit
    commit = commit.lstrip('g').strip()
    return tag, int(distance), commit, dirty


def read(*names, **kwargs):
    import os
    return open(
        os.path.join(os.path.dirname(__file__), *names),
        #encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='scanengine',
    version=get_version(),
    license='GPL-2.0',
    description=
        'scanengine is a copyright compliance tool powered by scanengine project.',
    #long_description=read('README.rst'),
    #author='clement_li',
    #url='https://gitee.com/meta-oss/FenixscanX',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
    keywords=[
        'open source', 'scan',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4',
    install_requires=[
        'more_itertools <  6.0.0; python_version == "2.7"',
        # end hack

        # cluecode
        # Some nltk version ranges are buggy
        'nltk >= 3.2, < 4.0',
        'py2_ipaddress >= 2.0, <3.5; python_version < "3"',
        'urlpy',
        'publicsuffix2',
        'fingerprints >= 0.6.0, < 1.0.0',

        # commoncode
        'commoncode >= 20.09',
        'backports.os == 0.1.1; python_version < "3"',

        'future >= 0.16.0',
        'saneyaml',

        # plugincode
        'plugincode',

        # licensedcode
        'bitarray >= 0.8.1, < 1.0.0',
        'intbitset >= 2.3.0,  < 3.0',
        'boolean.py >= 3.5,  < 4.0',
        'license_expression >= 0.99',
        'pyahocorasick >= 1.4, < 1.5',

        # multiple
        'lxml >= 4.0.0, < 5.0.0',

        # textcode
        'Beautifulsoup4 >= 4.0.0, <5.0.0',
        'html5lib',
        'six',
        'pdfminer.six >= 20170720',
        'pycryptodome >= 3.4',
        'chardet >= 3.0.0, <4.0.0',

        # typecode
        'typecode',

        # packagedcode
        'debut >= 0.9.4',
        'pefile >= 2018.8.8',
        'pymaven_patch >= 0.2.8',
        'requests >= 2.7.0, < 3.0.0',
        'packageurl_python >= 0.7.0',
        'xmltodict >= 0.11.0',
        'javaproperties >= 0.5',
        'toml >= 0.10.0',
        'gemfileparser >= 0.7.0',
        'pkginfo >= 1.5.0.1',
        'dparse2',
        'pygments >= 2.4.2, <2.5.1',

        # used to fix mojibake in Windows PE
        # for now we use the evrsion that works on both Python 2 and 3
        'ftfy <  5.0.0',

        # scanengine
        # Click 7.0 is broken https://github.com/pallets/click/issues/1125
        'click >= 6.7, !=7.0',
        'colorama >= 0.3.9',
        'pluggy >= 0.4.0, < 1.0',
        'attrs >= 18.1, !=20.1.0',
        'typing >=3.6, < 3.7',

        # scanengine outputs
        'jinja2 >= 2.7.0, < 3.0.0',
        'MarkupSafe >= 0.23',
        'simplejson',
        'spdx_tools >= 0.6.0',
        'unicodecsv',

        # scanengine caching and locking
        'yg.lockfile >= 2.3, < 3.0.0',
        # used by yg.lockfile
        'contextlib2', 'pytz', 'tempora', 'jaraco.functools',
        'zc.lockfile >= 2.0.0, < 3.0.0',
    ],

    extras_require={
        'full': [
            'extractcode',
            'extractcode_7z',
            'extractcode_libarchive',
            'typecode_libmagic',
        ],
    },

    entry_points={
        'console_scripts': [
            'scanengine = scanengine.cli:scanengine',
        ],

        # scanengine_pre_scan is the entry point for pre_scan plugins executed
        # before the scans.
        #
        # Each entry hast this form:
        #   plugin-name = fully.qualified.module:PluginClass
        # where plugin-name must be a unique name for this entrypoint.
        #
        # See also plugincode.pre_scan module for details and doc.
        'scanengine_pre_scan': [
            'ignore = scanengine.plugin_ignore:ProcessIgnore',
            'facet = summarycode.facet:AddFacet',
            'classify = summarycode.classify:FileClassifier',
        ],

        # scanengine_scan is the entry point for scan plugins that run a scan
        # after the pre_scan plugins and before the post_scan plugins.
        #
        # Each entry has this form:
        #   plugin-name = fully.qualified.module:PluginClass
        # where plugin-name must be a unique name for this entrypoint.
        #
        # IMPORTANT: The plugin-name is also the "scan key" used in scan results
        # for this scanner.
        #
        # See also plugincode.scan module for details and doc.
        'scanengine_scan': [
            'info = scanengine.plugin_info:InfoScanner',
            'licenses = licensedcode.plugin_license:LicenseScanner',
            'copyrights = cluecode.plugin_copyright:CopyrightScanner',
            'packages = packagedcode.plugin_package:PackageScanner',
            'emails = cluecode.plugin_email:EmailScanner',
            'urls = cluecode.plugin_url:UrlScanner',
            'generated = summarycode.generated:GeneratedCodeDetector',
        ],

        # scanengine_post_scan is the entry point for post_scan plugins executed
        # after the scan plugins and before the output plugins.
        #
        # Each entry hast this form:
        #   plugin-name = fully.qualified.module:PluginClass
        # where plugin-name must be a unique name for this entrypoint.
        #
        # See also plugincode.post_scan module for details and doc.
        'scanengine_post_scan': [
            'summary = summarycode.summarizer:ScanSummary',
            'summary-keeping-details = summarycode.summarizer:ScanSummaryWithDetails',
            'summary-key-files = summarycode.summarizer:ScanKeyFilesSummary',
            'summary-by-facet = summarycode.summarizer:ScanByFacetSummary',
            'license-clarity-score = summarycode.score:LicenseClarityScore',
            'license-policy = licensedcode.plugin_license_policy:LicensePolicy',
            'mark-source = scanengine.plugin_mark_source:MarkSource',
            'classify-package = summarycode.classify:PackageTopAndKeyFilesTagger',
            'is-license-text = licensedcode.plugin_license_text:IsLicenseText',
            'filter-clues = cluecode.plugin_filter_clues:RedundantCluesFilter',
            'consolidate = summarycode.plugin_consolidate:Consolidator',
        ],

        # scanengine_output_filter is the entry point for filter plugins executed
        # after the post-scan plugins and used by the output plugins to
        # exclude/filter certain files or directories from the codebase.
        #
        # Each entry hast this form:
        #   plugin-name = fully.qualified.module:PluginClass
        # where plugin-name must be a unique name for this entrypoint.
        #
        # See also plugincode.post_scan module for details and doc.
        'scanengine_output_filter': [
            'only-findings = scanengine.plugin_only_findings:OnlyFindings',
            'ignore-copyrights = cluecode.plugin_ignore_copyrights:IgnoreCopyrights',
        ],

        # scanengine_output is the entry point for output plugins that write a scan
        # output in a given format at the end of a scan.
        #
        # Each entry hast this form:
        #   plugin-name = fully.qualified.module:PluginClass
        # where plugin-name must be a unique name for this entrypoint.
        #
        # See also plugincode._output module for details and doc.
        'scanengine_output': [
            'html = formattedcode.output_html:HtmlOutput',
            'html-app = formattedcode.output_html:HtmlAppOutput',
            'json = formattedcode.output_json:JsonCompactOutput',
            'json-pp = formattedcode.output_json:JsonPrettyOutput',
            'spdx-tv = formattedcode.output_spdx:SpdxTvOutput',
            'spdx-rdf = formattedcode.output_spdx:SpdxRdfOutput',
            'csv = formattedcode.output_csv:CsvOutput',
            'jsonlines = formattedcode.output_jsonlines:JsonLinesOutput',
            'template = formattedcode.output_html:CustomTemplateOutput',
        ],
    },
)
