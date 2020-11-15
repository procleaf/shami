#! /usr/bin/env python3

# --------------------------------------------------------------------------
#
# Automation framework.
#
# yqm_leaf@163.com
#
# 07/14/19
#
# --------------------------------------------------------------------------

import os
import sys
import logging

from shami.log import setup_logging
from shami.task import TaskManager, Task

class AutomationFramework(object):
    def __init__(self):
        # setup logger.
        self.logger = setup_logging('system')

        self.task_manager = TaskManager()

    def start(self, daemon=False):
        """Start automation framework.
        :param daemon: whether or not daemonlize the framework.
        """
        self.logger.info("Automation framework started.")

    def run(self):
        """Call task manager to run all the tasks."""
        self.task_manager.scan_tasks()
        self.task_manager.run_tasks()

    def stop(self):
        """Stop automation framework."""
        self.logger.info("Automation framework stopped.")
