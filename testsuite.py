#! /usr/bin/env python

# --------------------------------------------------------------------------
#
# Test suite.
#
# yqm_leaf@163.com
#
# 07/14/19
#
# --------------------------------------------------------------------------

import os
import re
import logging

from shami.resource import Resource, ResourceManager
from shami.misc import DotResFile
from shami.utils import list_file
from shami.testcase import TestCase

class TestSuite(object):
    """Test suite class."""
    def __init__(self, suite_file):
        self.system_logger = logging.getLogger('system')
        self._suite_file = suite_file
        self.ts_basename = os.path.basename(self._suite_file)
        self.test_cases = []

    def start(self):
        """Start a test suite.
        :returns: Status of starting a test suite.
        """
        self.system_logger.info("Test suite %s started" % self._suite_file)

    def parse(self):
        """Parse test suite file.
        :returns: Dict of suite file.
        """
        pass

    def ask_rm_for_resource(self, requirement):
        """Ask resource manager for resource.
        :returns: List resource objects if enough resource, else None.
        """
        rm = ResourceManager()
        return rm.query_for_resource(requirement)

    def parse_dot_resource_file(self, dot_resource_file):
        """Parse dot resource file.
        :returns: Dict of dot resource file.
        """
        pass

    def parse_test_cases(self):
        """Parse test cases.
        :returns: List of test case objects.
        """
        test_cases = []
        suite_dir = os.path.dirname(self._suite_file)
        with open(self._suite_file) as f:
            for line in f:
                # skip comment lines.
                if re.search("^ *#", line):
                    continue
                m = re.match("(.*\.py$)", line, flags=re.IGNORECASE)
                if m:
                    test_case_file = m.group(1)
                    test_case_file = os.path.join(suite_dir, test_case_file)
                    if not os.path.isfile(test_case_file):
                        self.system_logger.debug("Test case file %s does not exist, skiping" %
                                                  test_case_file)
                        continue
                    test_case = TestCase(test_case_file)
                    test_cases.append(test_case)

        return test_cases

    def pass_suite(self):
        """Pass the test suite.
        :returns: None.
        """
        return True

    def fail_suite(self):
        """Fail the test suite.
        :returns: None.
        """
        return True

    def end(self):
        """End a test suite."""
        self.system_logger.info("Test suite %s ended" % self._suite_file)

    def __str__(self):
        return self.ts_basename
