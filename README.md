notifyme
========

This module is just a neat little context manager that can notify you via email
to your Gmail account when its body is completed.  Example usage:

```python
from notifyme import notify

with notify('Long, laborious task'):
    # Perform long, laborious task
```

Once the long, laborious task is done, you will receive an email saying "Long,
laborious task completed.".

Installation, Configuration, and Use
------------------------------------

Clone this repository, or just download `notifyme.py`.  Put `notifyme.py` in
your Python path.  Then, create a file in your home directory called `.notifyme`
with contents like the following:

    [email]:[password]

Don't include any whitespace.  Make sure your email includes "@gmail.com".
Then, change the permissions to 600 to protect your password:

```
chmod 600 ~/.notifyme
```

And you're done!  The Python code above should work perfectly.