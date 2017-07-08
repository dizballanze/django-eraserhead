=============================
Django Eraserhead
=============================

.. image:: https://badge.fury.io/py/django-eraserhead.svg
    :target: https://badge.fury.io/py/django-eraserhead

.. image:: https://travis-ci.org/dizballanze/django-eraserhead.svg?branch=master
    :target: https://travis-ci.org/dizballanze/django-eraserhead

.. image:: https://codecov.io/gh/dizballanze/django-eraserhead/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dizballanze/django-eraserhead

Provide hints to optimize database usage by deferring unused fields

Documentation
-------------

The full documentation is at https://django-eraserhead.readthedocs.io.

Quickstart
----------

Install Django Eraserhead::

    pip install django-eraserhead

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'eraserhead.apps.EraserheadConfig',
        ...
    )

Add Django Eraserhead's URL patterns:

.. code-block:: python

    from eraserhead import urls as eraserhead_urls


    urlpatterns = [
        ...
        url(r'^', include(eraserhead_urls)),
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
