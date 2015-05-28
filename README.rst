notifyme
========

This module is just a neat little context manager that can notify you via email
to your email account when its body is completed. Example usage:

.. code:: python

    from notifyme import notify

    with notify('Long, laborious task'):
        # Perform long, laborious task

Once the long, laborious task is done, you will receive an email saying “Long,
laborious task completed.”.

It also comes with a CLI. You simply run ``notifyme [command ...]`` to run the
command and get an email on completion.

Installation, Configuration, and Use
------------------------------------

To install, simply use the command ``pip install notifyme``. To configure this
module with your email server settings, create a file in your home directory
called ``.notifyme`` with contents like the following:

::

    [default]
    email = <your-email-here>
    host = <smtp-hostname-here>
    port = <smtp-port-here>
    username = <only-if-different-from-email>
    password = <password-here>
    security = <SSL or TLS or NONE>

You’ll have to look up your configuration details from your email
provider. After you fill this out and save it, you’ll also want to protect it
from access by other users, which you can do with the following command:

::

    chmod 600 ~/.notifyme

And you’re done!  You can now use the module within Python code as a context
manager, or on the command line for any program you'd like.

License
-------

This project is released under the Revised BSD license.  See ``LICENSE.txt`` for
details.
