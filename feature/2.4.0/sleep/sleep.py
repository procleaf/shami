#! /usr/bin/env python

# ------------------------------------------------------------------------------
#
# Test case sleep.
#
# yqm_leaf@163.com
#
# 07/19/19
#
# ------------------------------------------------------------------------------

import time
import logging
import sys
import os
from datetime import datetime

from shami.error import TestCaseFailed
from shami.log import setup_logging
from shami.misc import upload_logfile
from shami.mail import Mail

# setup logging.
log_file_basename = os.path.basename(os.path.splitext(__file__)[0])

log_name = log_file_basename
log_file_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_file_dir, log_file_basename)
now = datetime.now()
time_str = now.strftime("%Y_%m_%d_%H_%M_%S")

log_file = log_file + '_' + time_str + '.log'

logger = logging.getLogger(log_name)
logger.setLevel(logging.DEBUG)
log_file = os.path.join(os.path.dirname(__file__), log_file)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fd = logging.FileHandler(log_file)
fd.setLevel(logging.DEBUG)
fd.setFormatter(formatter)
logger.addHandler(fd)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
# end of log setup.

sec = 10
logger.info("This test case sleep for %d secs" % sec)
time.sleep(sec)
logger.info('Uploading log file: %s' % log_file)
upload_logfile(log_file)
raise TestCaseFailed
