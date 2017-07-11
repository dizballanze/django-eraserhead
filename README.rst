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

.. image:: https://github.com/dizballanze/django-eraserhead/raw/master/eraserhead.jpg

Documentation
-------------

Requirements
-----------

* Django 1.9+
* Python 2.7, 3.4+

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

    ERASERHEAD_ENABLED = True
    ERASERHEAD_TRACEBACK_BASE_PATH = BASE_DIR


Settings:

* `ERASERHEAD_ENABLED` - enable/disable Django Eraserhead
* `ERASERHEAD_TRACEBACK_BASE_PATH` - set base path to filter tracebacks. Set to `None` to display full traceback.

Features
--------

.. image:: https://github.com/dizballanze/django-eraserhead/raw/master/screenshot.png

Django Eraserhead monitors:

* querysets/models fields usage (used and unused fields) with considering deferred fields
* count of instances created for each queryset
* corresponding model of each queryset
* traceback for each queryset to easily find corresponding code

Based on fields usage Django Eraserhead suggests optimizations for each queryset.


TODO
-----

* calculate memory consumption of unused fields
* decorator and/or context processor for partial stats collecting
* detect deferred fields loading
* auto deferring fields based on usage

Running Tests
-------------

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
