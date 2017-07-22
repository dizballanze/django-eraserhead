try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from django.test import TestCase

from eraserhead.request_storage import RequestStorage


class RequestStorageTestCase(TestCase):

    def setUp(self):
        super(RequestStorageTestCase, self).setUp()
        self.request_storage = RequestStorage()
        self.queryset_storage = Mock()

    def test_add_queryset_storage_instance(self):
        """ Should add queryset storage to the instance attribute """
        self.request_storage.add_queryset_storage_instance(self.queryset_storage)
        self.assertIn(self.queryset_storage, self.request_storage.queryset_stats)
