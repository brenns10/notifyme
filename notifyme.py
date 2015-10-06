#!/usr/bin/env python3
"""
Simple module for email notifications when a task is finished.

This module supports sending mail via any mail server (not just Gmail anymore)
by employing a better configuration file.  The configuration file must contain
a "default" section, as well as any additional profiles you may wish to send
to.  You should include the following items in every profile section:

- email: your email address.
- host: SMTP server hostname.
- port: SMTP server port.
- username: (if different from email) **not required
- password: your password (trailing whitespace is an issue!)
- security: SSL, TLS, or None.
"""

from contextlib import contextmanager
from os.path import expanduser, expandvars
from smtplib import SMTP, SMTP_SSL
from configparser import ConfigParser
from timeit import default_timer

import sys
import socket
import subprocess


CONF_FILE = '~/.notifyme'


class NotifyMeMailer(object):
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
        if self._security == 'SSL':
            return SMTP_SSL(self._hostname, self._port)

        smtp = SMTP(self._hostname, self._port)
        if self._security == 'TLS':
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
    time = default_timer()

    # Pass control to the caller.
    yield

    # Send the notification.
    time = default_timer() - time
    msg = '\nWall Time: %0.4f s' % time
    print(msg)
    subject = task_name + ' completed.'
    handler.send(subject, subject + msg)


def _check_args():
    if not sys.argv[1:]:
        print('No command specified.')
        print('Usage: %s [command ...]' % sys.argv[0])
        print('Notifies on completion of a command.')
        sys.exit(1)


def _main():
    """
    Main for CLI notification process.

    Call notifyme.py with a command.  When the command completes, you will be
    emailed.
    """

    _check_args()

    profile = 'default'
    if sys.argv[1].startswith('--profile='):
        profile = sys.argv[1][len('--profile='):]
        del sys.argv[1]

    _check_args()

    hostname = socket.gethostname()
    args = sys.argv[1:]

    with notify("Command \"%s\" ON \"%s\"" % (args[0], hostname),
                profile=profile):
        code = subprocess.call(args)
        sys.stdout.flush()
        sys.stderr.flush()

    sys.exit(code)


if __name__ == '__main__':
    _main()
