#! /usr/bin/env python3

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
