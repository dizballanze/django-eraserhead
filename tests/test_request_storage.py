try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from django.test import TestCase

from eraserhead.request_storage import RequestStorage


class RequestStorageTestCase(TestCase):

    def test_add_queryset_storage_instance(self):
        """ Should add queryset storage to the instance attribute """
        request_storage = RequestStorage()
        queryset_storage = Mock()
        request_storage.add_queryset_storage_instance(queryset_storage)
        self.assertIn(queryset_storage, request_storage.queryset_stats)

    def test_total_wasted_memory(self):
        """ Should return total wasted memory for all querysets """
        qs_storage1 = Mock()
        qs_storage1.total_wasted_memory = 500
        qs_storage2 = Mock()
        qs_storage2.total_wasted_memory = 3600
        request_storage = RequestStorage()
        request_storage.add_queryset_storage_instance(qs_storage1)
        request_storage.add_queryset_storage_instance(qs_storage2)
        self.assertEqual(request_storage.total_wasted_memory, 4100)
