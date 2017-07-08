=====
Usage
=====

To use Django Eraserhead in a project, add it to your `INSTALLED_APPS`:

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
