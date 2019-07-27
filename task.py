#! /usr/bin/env python

# --------------------------------------------------------------------------
#
# Task manager.
#
# yqm_leaf@163.com
#
# 07/14/19
#
# --------------------------------------------------------------------------

import os
import re
import logging
from email.mime.text import MIMEText
import traceback
import sqlite3

from shami.utils import get_cwd, list_file
from shami.log import Logger
from shami.testsuite import TestSuite
from shami.misc import DotResFile
from shami.resource import Resource, ResourceManager
from shami.mail import Mail

class TaskManager(object):
    """Task manager."""

    def __init__(self):
        self.logger = logging.getLogger('system')
        self.task_dict = {}

    def scan_tasks(self, task_dir=None):
        """
        Scan for tasks.
        :param task_dir: where task files resides.
        """
        if task_dir is None:
            # default task dir.
            task_dir = os.path.join(get_cwd(), 'tasks')

        for task_file in list_file(task_dir):
            if task_file.endswith(('.old', '.OLD')) or \
               task_file.endswith(('.running', '.RUNNING')) or \
               task_file.endswith(('.task', '.TASK')):
                t = self.create_task(task_file)
                if t is None:
                    self.logger.error("Create task instance with file: %s failed." %\
                            task_file, exc_info=True)

    def run_tasks(self):
        """
        Run tasks.
        """
        for task_file, task in self.task_dict.items():
            if task_file.endswith(('.task', '.TASK')):
                self.logger.info("Task file found: %s" % task_file)
                pid = os.fork()
                if pid == 0:
                    if not task.run():
                        self.logger.error("Task %s failed to run." % task, exc_info=True)
                    # The exit statement os.exit(0) of the child function is 
                    # necessary, because otherwise the child process would return 
                    # into the parent process, i.e. to the input statement.
                    # https://www.python-course.eu/forking.php
                    os._exit(0)
                else:
                    pass
                    #os.waitpid(pid, 0)

        return True

    def create_task(self, task_file):
        """
        Create a task instance and put it into self.task_dict.
        :param task_file: path to a task file.
        """
        task = None
        if task_file in self.task_dict:
            task = self.task_dict[task_file]
        else:
            task = Task(task_file)
            task.manager = self
            self.task_dict[task_file] = task

        return task

    def list(self):
        """
        List all tasks.
        """
        for task_file in self.task_dict.keys():
            print(task_file)

    def list_new(self):
        """
        List new tasks.
        """
        for task_file in self.task_dict.keys():
            if task_file.endswith(('.task', '.TASK')):
                print(task_file)

    def list_running(self):
        """
        List running tasks.
        """
        for task_file in self.task_dict.keys():
            if task_file.endswith(('.running', '.RUNNING')):
                print(task_file)


    def list_old(self):
        """
        List old tasks.
        """
        for task_file in self.task_dict.keys():
            if task_file.endswith(('.old', '.OLD')):
                print(task_file)

class Task(object):

    def __init__(self, task_file):
        # TODO: merge these loggers into one.
        self.logger = logging.getLogger('system')
        self.logger_class = Logger()
        self._task_file = task_file
        self.mailer = Mail()
        self.task_passed = None
        self.manager = None

    def __str__(self):
        return os.path.basename(os.path.splitext(self._task_file)[0])

    def run(self):
        """
        Run task.
        """
        task_dict = self.parse()
        feature_dir = os.path.join(get_cwd(), 'feature')

        test_suite_file = os.path.join(feature_dir, 
                task_dict['version'], task_dict['feature'],
                task_dict['feature'] + '.suite')
        dot_resource_file = os.path.join(feature_dir, 
                task_dict['version'], task_dict['feature'],
                task_dict['feature'] + '.suite')

        if not os.path.isfile(test_suite_file):
            self.logger.info("Test suite file: %s does not exist, aborting." %\
                             test_suite_file)
            return False

        
        # Parse dot resource file.
        dot_resource = DotResFile(dot_resource_file)
        requirement = dot_resource.parse()

        # Acquire resource.
        rm = ResourceManager()
        resources = rm.acquire_resource(requirement)

        if resources is None:
            self.logger.info("Not enought resource to run task: %s" % 
                             os.path.basename(self._task_file))
            return False

        # Use test suite to parse to-be-run test cases.
        test_suite = TestSuite(test_suite_file)

        # Get test cases.
        test_cases = test_suite.parse_test_cases()
        
        # Start task.
        self.start()

        mail_body = ''
        try:
            # Run test cases.
            for t in test_cases:
                t_result = t.run()
                if t_result is False:
                    self.task_passed = False
                    for line in traceback.format_stack():
                        mail_body = mail_body + line.strip()
                    msg = MIMEText(mail_body)
                    msg['Subject'] = '%s failed' % os.path.basename(self._task_file)
                    self.mailer.send(msg)
                    # TODO: change this to real data.
                    task_dict['logurl'] = 'http://localhost/logurl'
                    self.logger_class.insert_log_to_db(task_dict)

                    # If one of the test cases fails, fail the whole task and
                    # return immeidiately.
                    return False
        finally:
            # Release resources.
            if not rm.release_resource(resources):
                raise ReleaseResourceError(resource.resource_file)
            self.end()

        msg = MIMEText('')
        msg['Subject'] = '%s passed' % os.path.basename(self._task_file)
        self.mailer.send(msg)

        # TODO: change this to real data.
        task_dict['logurl'] = 'http://localhost/logurl'
        self.logger_class.insert_log_to_db(task_dict)

        return True

    def start(self):
        """Start task.
        :returns: status of starting task.
        """
        self.logger.info("Task %s started" % self._task_file)
        # Change .task file to .task.running.
        os.rename(self._task_file, self._task_file + '.running')

    def end(self):
        """End task.
        :returns: status of ending task.
        """
        # Change .task file to .task.running.
        os.rename(self._task_file + '.running', self._task_file + 
                '.old')
        self.logger.info("Task %s ended" % self._task_file)


    def parse(self):
        """Parse task file.
        :returns: dict of task file.
        """
        task_dict = {}
        with open(self._task_file) as f:
            for line in f:
                # Skip comment lines.
                if re.search(" *#", line):
                    continue
                m = re.match(r"^version: *([0-9\.]+)", line)
                if m:
                    task_dict['version'] = m.group(1)

                m = re.match(r"^feature: *([a-zA-Z0-9 \.]+)", line)
                if m:
                    # change space to underscore.
                    task_dict['feature'] = re.sub(r' ', '_', m.group(1))

                m = re.match(r"^tester: *([a-zA-Z0-9 \.]+)", line)
                if m:
                    task_dict['tester'] = m.group(1)
        return None if task_dict is {} else task_dict
