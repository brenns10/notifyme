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
from smtplib import SMTP_SSL

CONF_FILE = '~/.notifyme'
HOST = 'smtp.gmail.com'
PORT = 465


@contextmanager
def notify(task_name, conf=CONF_FILE):
    """Context manager that sends an email notification on completion of body.

    See module documentation for configuration.

    Parameters:
    - task_name: Name of the task to use in the email notification.
    - conf: Alternative config file.  Supports environment variables and ~.

    """
    # Open the configuration and read it.
    config = expanduser(expandvars(conf))
    with open(config, 'r') as f:
        config_line = f.readline()
    email, password = config_line.split(':', 1)

    # Pass control to the caller.
    yield

    # On exit, connect to SMTP server over SSL and send email alert.
    smtp = SMTP_SSL(HOST, PORT)
    smtp.login(email, password)

    subject = task_name + ' completed.'

    message = "From: %s\r\n"    \
              "To: %s\r\n"      \
              "Subject: %s\r\n" \
              "\r\n"            \
              "%s" % (email, email, subject, subject)

    smtp.sendmail(email, email, message)
    smtp.quit()
