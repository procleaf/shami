#! /usr/bin/env python3

# --------------------------------------------------------------------------
#
# List tasks.
#
# yqm_leaf@163.com
#
# 07/17/19
#
# --------------------------------------------------------------------------

from shami.task import TaskManager

tm = TaskManager()
tm.scan_tasks()
tm.list()
