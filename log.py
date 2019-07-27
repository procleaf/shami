#! /usr/bin/env python

# --------------------------------------------------------------------------
#
# Logger.
#
# yqm_leaf@163.com
#
# 07/14/19
#
# --------------------------------------------------------------------------

import logging
import logging.handlers
import sys
import os
import traceback
import sqlite3

from shami.utils import get_cwd, getenv
from shami.config import get_config

class Logger(object):

    def __init__(self, stream=sys.stdout):
        self._cf = get_config()
        self.wd = getenv('SHAMI')
        self.logtableengine = self._cf['log']['engine']
        self.logtablefile = os.path.join(self.wd, self._cf['log']['db_file'])
        self.logtablename = self._cf['log']['table']
        self.stream = stream

    def init_log_table(self):
        """
        Initialize log table in the database.
        """
        conn = sqlite3.connect(self.logtablefile)
        
        c = conn.cursor()
        
        c.execute('''CREATE TABLE %s 
                (ID INT PRIMARY KEY,
                 TESTER         VARCHAR(20) NOT NULL,
                 FEATURE        VARCHAR(20) NOT NULL,
                 VERSION        VARCHAR(20) NOT NULL,
                 LOGURL         VARCHAR(50) NOT NULL
                );''' % self.logtablename)
        
        conn.commit()
        conn.close()

    def insert_log_to_db(self, dict):
        """
        Insert test entry into database.
        :param dict: task dict
        """
        conn = sqlite3.connect(self.logtablefile)
        c = conn.cursor()
        sql = "INSERT INTO shamilog VALUES (NULL, '{0}', '{1}', '{2}', '{3}');".format(
                dict['tester'], dict['feature'],
                dict['version'], dict['logurl'])

        c.execute(sql)
        conn.commit()
        conn.close()

    def _write(self, msg):
        """
        Low level write method.
        :param msg: message to be wrttien.
        """
        self.stream.write("%s\n" % msg)

    def info(self, msg):
        """
        Log system information.
        :param msg: message to be logged.
        """
        self._write(msg)

    def sys(self, msg):
        """
        Log system information.
        :param msg: message to be logged.
        """
        self._write(msg)

def setup_logging(name, file=None, log_to_console=True):
    """
    Setup logging.
    :param name: name of the logger.
    :param file: file for FileHandler.
    :param log_to_console: whether or not log to console.
    """
    if file is None:
        file = name + '.log'
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    log_file = os.path.join(os.path.dirname(__file__), file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Add log rotation.  Max bytes is 2MB.
    rotate_handler = logging.handlers.RotatingFileHandler(
                          log_file, maxBytes=2000000, backupCount=5)
    fd = logging.FileHandler(log_file)
    fd.setLevel(logging.DEBUG)
    fd.setFormatter(formatter)
    logger.addHandler(fd)
    logger.addHandler(rotate_handler)

    if log_to_console:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
