=============
Configuration
=============

Configurations can be set as environment variables and as Django settings too (in case your project uses Django.

The variables are:

CELERY_PERSISTENT_REVOKES_BACKEND:
    Default value: 'celery_persistent_revokes.backends.DjangoDatabase'. This variable defines the backend used to store and fetch the tasks ids of the tasks you revoke using this package.


CELERY_PERSISTENT_REVOKES_MODEL:
    Default value: 'celery_persistent_revokes.CeleryTaskRevoke'. If you're using DjangoDatabase backend, you can use this variable to define another Django model to store your Revokes.

    .. code-block:: python

        from django.db import models
        from celery_persistent_revokes.models import CeleryTaskRevoke

        class MyCustomRevoke(CeleryTaskRevoke)
            created = models.DateTimeField(auto_now=True)
