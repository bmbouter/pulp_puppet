#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2012 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
import os
import subprocess

from pulp.devel.test_runner import run_tests

# Find and eradicate any existing .pyc files, so they do not eradicate us!
PROJECT_DIR = os.path.dirname(__file__)
subprocess.call(['find', PROJECT_DIR, '-name', '*.pyc', '-delete'])

PACKAGES = [os.path.dirname(__file__), 'pulp_puppet']

TESTS = [
    'pulp_puppet_common/test/unit/',
    'pulp_puppet_extensions_admin/test/unit/',
    'pulp_puppet_extensions_consumer/test/unit/',
    'pulp_puppet_handlers/test/unit/',
]

PLUGIN_TESTS = ['pulp_puppet_plugins/test/unit/']

dir_safe_all_platforms = [os.path.join(os.path.dirname(__file__), x) for x in TESTS]
dir_safe_non_rhel5 = [os.path.join(os.path.dirname(__file__), x) for x in PLUGIN_TESTS]

os.environ['DJANGO_SETTINGS_MODULE'] = 'pulp_puppet.forge.settings'

run_tests(PACKAGES, dir_safe_all_platforms, dir_safe_non_rhel5)
