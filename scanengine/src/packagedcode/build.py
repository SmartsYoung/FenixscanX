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
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
from collections import OrderedDict
import ast
import logging
import os

import attr

from commoncode import filetype
from commoncode import fileutils
from packagedcode import models
from packagedcode.utils import combine_expressions
from scanengine.api import get_licenses


TRACE = False

logger = logging.getLogger(__name__)

if TRACE:
    import sys
    logging.basicConfig(stream=sys.stdout)
    logger.setLevel(logging.DEBUG)


"""
Detect as Packages common build tools and environment such as Make, Autotools,
gradle, Buck, Bazel, Pants, etc.
"""


@attr.s()
class BaseBuildManifestPackage(models.Package):
    metafiles = tuple()

    @classmethod
    def recognize(cls, location):
        if not cls._is_build_manifest(location):
            return

        # we use the parent directory as a name
        name = fileutils.file_name(fileutils.parent_directory(location))
        # we could use checksums as version in the future
        version = None

        # there is an optional array of license file names in targets that we could use
        # declared_license = None
        # there is are dependencies we could use
        # dependencies = []
        yield cls(
            name=name,
            version=version)

    @classmethod
    def get_package_root(cls, manifest_resource, codebase):
        return manifest_resource.parent(codebase)

    @classmethod
    def _is_build_manifest(cls, location):
        if not filetype.is_file(location):
            return False
        fn = fileutils.file_name(location)
        return any(fn == mf for mf in cls.metafiles)


@attr.s()
class AutotoolsPackage(BaseBuildManifestPackage):
    metafiles = ('configure', 'configure.ac',)
    default_type = 'autotools'


starlark_rule_types = [
    'binary',
    'library'
]


@attr.s()
class StarlarkManifestPackage(BaseBuildManifestPackage):
    @classmethod
    def recognize(cls, location):
        if not cls._is_build_manifest(location):
            return

        # Thanks to Starlark being a Python dialect, we can use the `ast`
        # library to parse it
        with open(location, 'rb') as f:
            tree = ast.parse(f.read())

        build_rules = defaultdict(list)
        for statement in tree.body:
            # We only care about function calls or assignments to functions whose
            # names ends with one of the strings in `rule_types`
            if (isinstance(statement, ast.Expr)
                    or isinstance(statement, ast.Call)
                    or isinstance(statement, ast.Assign)
                    and isinstance(statement.value, ast.Call)
                    and isinstance(statement.value.func, ast.Name)
                    and statement.value.func.id.endswith(starlark_rule_types)):
                rule_name = statement.value.func.id
                # Process the rule arguments
                args = OrderedDict()
                for kw in statement.value.keywords:
                    arg_name = kw.arg
                    if isinstance(kw.value, ast.Str):
                        args[arg_name] = kw.value.s
                    if isinstance(kw.value, ast.List):
                        # We collect the elements of a list if the element is not a function call
                        args[arg_name] = [elt.s for elt in kw.value.elts if not isinstance(elt, ast.Call)]
                if args:
                    build_rules[rule_name].append(args)

        if build_rules:
            for rule_name, rule_instances_args in build_rules.items():
                for args in rule_instances_args:
                    name = args.get('name')
                    if not name:
                        continue
                    license_files = args.get('licenses')
                    yield cls(
                        name=name,
                        declared_license=license_files,
                        root_path=fileutils.parent_directory(location)
                    )
        else:
            # If we don't find anything in the manifest file, we yield a Package with
            # the parent directory as the name
            yield cls(
                name=fileutils.file_name(fileutils.parent_directory(location))
            )

    def compute_normalized_license(self):
        """
        Return a normalized license expression string detected from a list of
        declared license items.
        """
        declared_license = self.declared_license
        manifest_parent_path = self.root_path

        if not declared_license or not manifest_parent_path:
            return

        license_expressions = []
        for license_file in declared_license:
            license_file_path = os.path.join(manifest_parent_path, license_file)
            if os.path.exists(license_file_path) and os.path.isfile(license_file_path):
                licenses = get_licenses(license_file_path)
                license_expressions.extend(licenses.get('license_expressions', []))

        return combine_expressions(license_expressions)


@attr.s()
class BazelPackage(StarlarkManifestPackage):
    metafiles = ('BUILD',)
    default_type = 'bazel'


@attr.s()
class BuckPackage(StarlarkManifestPackage):
    metafiles = ('BUCK',)
    default_type = 'buck'
