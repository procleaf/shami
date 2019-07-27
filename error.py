#! /usr/bin/env python

# --------------------------------------------------------------------------
#
# Exception classes.
#
# yqm_leaf@163.com
#
# 07/19/19
#
# --------------------------------------------------------------------------

class ReleaseResourceError(Exception):
    pass

class FileNotFound(Exception):
    pass

class TestCaseFailed(Exception):
    """
    Test case failed.
    """
    pass
