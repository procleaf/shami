#! /usr/bin/env python

# --------------------------------------------------------------------------
#
# Configuration.
#
# yqm_leaf@163.com
#
# 07/14/19
#
# --------------------------------------------------------------------------

import configparser
import os

class Config(object):
    def __init__(self):
        pass

def get_config():
    """
    Return configparser object.
    """
    cf = configparser.ConfigParser()
    config_file = os.path.join(os.environ.get('SHAMI'), 'config.ini')
    cf.read(config_file)
    return cf
