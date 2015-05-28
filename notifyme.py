#!/usr/bin/env python3
"""Simple module for email notifications when a task is finished.

Currently only supports Gmail, over SMTP_SSL.  Requires a configuration file
(~/.notifyme by default) to specify the email address and password.  I
recommend using 2-step authentication and an app-specific password (which works
perfectly with this module).  Also, set the permissions to 600 for better
security.  The config file should look like this:

    [email]:[password]

There should be no extraneous whitespace.  The email address should include
'@gmail.com'.

"""

from contextlib import contextmanager
from os.path import expanduser, expandvars
from smtplib import SMTP, SMTP_SSL
from configparser import ConfigParser

import sys
import socket
import os


CONF_FILE = '~/.notifyme'
HOST = 'smtp.gmail.com'
PORT = 465


def NotifyMeMailer(object):
    """Class that handles SMTP functions using the configuration file."""

    def __init__(self, conf=CONF_FILE, profile='default'):
        """
        Create a mailer from a configuration file and profile.

        :param conf: The location of the configuration file, which contains all
        important values for opening an SMTP connection.
        :param profile: Name of the profile (which is just a header in the
        configuration file) to send from and to.
        """
        self._conf = conf
        self._profile = profile

        self._parse_config()

    def _parse_config(self):
        """Parse the configuration file!"""
        parser = ConfigParser()
        parser.read(self._conf)
        profile = parser[self._profile]

        self._email = profile['email']
        self._hostname = profile['host']
        self._username = profile.get('email', self._email)
        self._password = profile['password']
        self._port = int(profile['port'])
        self._security = profile.get('security', 'none').upper()

    def _get_smtp(self):
        """Return the correct instance of SMTP for the required security."""
        if self.security == 'SSL':
            return SMTP_SSL(self._hostname, self._port)

        smtp = SMTP(self._hostname, self._port)
        if self.security == 'TLS':
            smtp.starttls()
        return smtp

    def send(self, subject, body):
        """Login, send a message to yourself, and exit."""
        message = "From: %s\r\n"     \
                  "To: %s\r\n"       \
                  "Subject: %s\r\n"  \
                  "\r\n"             \
                  "%s" % (self._email, self._email, subject, body)

        smtp = self._get_smtp()
        smtp.login(self._username, self._password)
        smtp.sendmail(self._email, self._email, message)
        smtp.quit()


@contextmanager
def notify(task_name, conf=CONF_FILE, profile='default'):
    """
    Context manager that sends an email notification on completion of body.

    See module documentation for configuration.

    Parameters:
    - task_name: Name of the task to use in the email notification.
    - conf: Alternative config file.  Supports environment variables and ~.
    """
    # Open the configuration and read it!
    config = expanduser(expandvars(conf))
    handler = NotifyMeMailer(conf=config, profile=profile)

    # Pass control to the caller.
    yield

    # Send the notification.
    subject = task_name + ' completed.'
    handler.send(subject, subject)


def _main():
    """
    Main for CLI notification process.

    Call notifyme.py with a command.  When the command completes, you will be
    emailed.
    """

    if not sys.argv[1:]:
        print('No command specified.')
        print('Usage: %s [command ...]' % sys.argv[0])
        print('Notifies on completion of a command.')
        sys.exit(1)

    hostname = socket.gethostname()
    command = ' '.join(sys.argv[1:])

    with notify("COMMAND [%s] ON \"%s\"" % (command, hostname)):
        # Use os.system() because this is one of the few times when we actually
        # *do* want to spawn a subshell, execute an arbitrary command, and send
        # output/errors to stdout and stderr!
        code = os.system(command)
        sys.stdout.flush()
        sys.stderr.flush()

    sys.exit(code)


if __name__ == '__main__':
    _main()
