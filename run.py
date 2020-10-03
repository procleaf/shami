#! /usr/bin/env python3

# --------------------------------------------------------------------------
#
# Run automation framework.
#
# yqm_leaf@163.com
#
# 07/14/19
#
# --------------------------------------------------------------------------

import sys
import os

from shami.af import AutomationFramework
    
af = AutomationFramework()
af.start()
af.run()
af.stop()
