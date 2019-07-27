#! /usr/bin/env python

# --------------------------------------------------------------------------
#
# Utilities.
#
# yqm_leaf@163.com
#
# 07/14/19
#
# --------------------------------------------------------------------------

import os

def list_file(directory):
    """List files in a directory.
    :returns: yields file full path.
    """
    for root, d, files in os.walk(directory):
        for f in files: yield os.path.join(root, f)

def get_cwd():
    """
    Get current working directory.
    """
    return os.path.dirname(__file__)

def execfile(file):
    with open(file) as f:
        code = compile(f.read(), file, 'exec')
        exec(code)
def getenv(env):
    """
    Get environment variable.
    """
    return os.environ.get(env)
