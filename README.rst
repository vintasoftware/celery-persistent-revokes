=============================
Celery Persistent Revokes
=============================

.. image:: https://badge.fury.io/py/celery-persistent-revokes.svg
    :target: https://badge.fury.io/py/celery-persistent-revokes

.. image:: https://travis-ci.org/hugobessa/celery-persistent-revokes.svg?branch=master
    :target: https://travis-ci.org/hugobessa/celery-persistent-revokes

.. image:: https://codecov.io/gh/hugobessa/celery-persistent-revokes/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/hugobessa/celery-persistent-revokes

Celery task revokes are stored on memory or on file. This packages makes possible to easely customize how your revokes are stored (Ex.: Database).

Documentation
-------------

The full documentation is at https://celery-persistent-revokes.readthedocs.io.

Quickstart
----------

Install Celery Persistent Revokes::

    pip install celery-persistent-revokes

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'celery_persistent_revokes.apps.CeleryPersistentRevokesConfig',
        ...
    )

Add Celery Persistent Revokes's URL patterns:

.. code-block:: python

    from celery_persistent_revokes import urls as celery_persistent_revokes_urls


    urlpatterns = [
        ...
        url(r'^', include(celery_persistent_revokes_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
