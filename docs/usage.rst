=====
Usage
=====

To use Celery Persistent Revokes in a project, add it to your `INSTALLED_APPS`:

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
