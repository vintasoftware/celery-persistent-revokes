=====
Usage
=====


Django Projects
---------------

To use Celery Persistent Revokes in a Django project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'celery_persistent_revokes.apps.CeleryPersistentRevokesConfig',
        ...
    )

Run migrations:

.. code-block::

    $ python manage.py migrate celery_persistent_revokes


Use ``revokable_task()`` decorator to create tasks:

.. code-block:: python

    from celery_persistent_revokes.decorators import revokable_task


    @revokable_task(my_celery_app)
    def my_pretty_task(my_arg):
        do_something(my_arg)
        return


Use ``revoke()`` helper to create tasks:

.. code-block:: python

    from celery_persistent_revokes.helpers import revoke

    result = my_pretty_task.delay()

    # ...

    revoke(result.id)


Other Python Projects
---------------------

To use Celery Persistent Revokes without Django, you need to implement your own task management backend. But don't panic, this is pretty straight forward:

.. code-block:: python

    class MyCustomBackend(object):

        def revoke(self, task_id):
            # save on your storage the id of the task to be revoked

        def list_revokes(self):
            # list the ids of your revoked tasks

        def is_task_revoked(self, task_id):
            # returns True if the task with the id equal to task_id
            # is marked as revoked in your storage

        def delete_revoke(self, task_id):
            # removes the revoked task with id equal to task_id from
            # your storage


Then you just need to set the path to MyCustomBackend in an environment variable called CELERY_PERSISTENT_REVOKES_BACKEND.

Supposing that you have the following file structure and MyCustomBackend is in a task_revoke_backends module:

.. code-block:: bash

    $ export CELERY_PERSISTENT_REVOKES_BACKEND='task_revoke_backends.MyCustomBackend'

