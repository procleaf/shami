#! /usr/bin/env python

# --------------------------------------------------------------------------
#
# Resource & resource manager.
#
# yqm_leaf@163.com
#
# 07/15/19
#
# --------------------------------------------------------------------------

import re
import ftplib
import os

from shami.config import get_config

class DotResFile(object):

    def __init__(self, dot_res_file):
        self.dot_res_file = dot_res_file
        pass

    def parse(self):
        """
        Parse '.res' file.
        :returns: requirements.
        """
        d = {}
        with open(self.dot_res_file) as f:
            for line in f:
                # Skip comment lines.
                if re.search(" *#", line):
                    continue
                m = re.match(r"(\w+) *= *(\w+)", line)
                if m:
                    k, v = m.group(1), m.group(2)
                    d[k] = v

        return d if d is not {} else None

def upload_logfile(logfile):
    """
    Upload log file to server.
    """
    cf = get_config()
    section = cf['ftp']
    server = section['server']
    user = section['user']
    password = section['password']
    directory = section['directory']

    session = ftplib.FTP(server, user, password)
    session.cwd(directory)
    file = open(logfile, 'rb')
    session.storlines("STOR " + os.path.basename(logfile), file)
    file.close()
    session.quit()
