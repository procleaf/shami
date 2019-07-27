#! /usr/bin/env python

# --------------------------------------------------------------------------
#
# Test case.
#
# yqm_leaf@163.com
#
# 07/14/19
#
# --------------------------------------------------------------------------

import logging

from shami.utils import execfile
from shami.error import TestCaseFailed

class TestCase(object):
    """Test case class."""
    def __init__(self, test_case):
        self.system_logger = logging.getLogger('system')
        self.test_case = test_case

    def __str__(self):
        return self.test_case

    def start(self):
        """Start a test case.
        :returns: Status of starting test case."""
        self.system_logger.info("Test case %s started." % self.test_case)

    def end(self):
        """End a test case.
        :returns: Status of ending test case.
        """
        self.system_logger.info("Test case %s ended." % self.test_case)

    def pass_case(self):
        """Pass test case.
        :returns: True.
        """
        self.system_logger.info("Test case %s passed." % self)

    def fail_case(self):
        """Fail test case.
        :returns: False.
        """
        self.system_logger.info("Test case %s failed." % self)

    def run(self):
        """Run case.
        :returns: None.
        """
        try:
            self.start()
            execfile(self.test_case)
        except TestCaseFailed:
            # Test case failed.
            self.pass_case()
            return False
        else:
            # Test case passed.
            self.fail_case()
            return True
        finally:
            self.end()

        return True
