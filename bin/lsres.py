#! /usr/bin/env python

# --------------------------------------------------------------------------
#
# List resources.
#
# yqm_leaf@163.com
#
# 07/18/19
#
# --------------------------------------------------------------------------

from shami.resource import ResourceManager

rm = ResourceManager()
for i in rm.list():
    print(i)
