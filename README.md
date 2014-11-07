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