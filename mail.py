#! /usr/bin/env python

# --------------------------------------------------------------------------
#
# Mail service.
#
# yqm_leaf@163.com
#
# 07/18/19
#
# --------------------------------------------------------------------------

import smtplib
import smtplib
from email.mime.text import MIMEText

from shami.config import get_config

class Mail(object):
    """
    Send emails.
    """
    def __init__(self):
        self._cf = get_config()
        self._mail_sec = self._cf['mail']

        self.sender = self._mail_sec['sender']
        self.receiver = self._mail_sec['receiver']
        self.port = self._mail_sec['port']
        self.mail_server = self._mail_sec['server']

    def send(self, msg=None):
        """
        Send mail.
        """
        if msg is None:
            return
        msg['From'] = self.sender
        msg['To'] = self.receiver
        with smtplib.SMTP(self.mail_server, self.port) as server:
            server.sendmail(self.sender, self.receiver, msg.as_string())
