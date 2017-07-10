from unittest.mock import Mock

from django.test import TestCase

from eraserhead.request_storage import RequestStorage


class RequestStorageTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.request_storage = RequestStorage()
        self.tb = Mock()
        self.queryset = Mock()

    def test_add_queryset_instance(self):
        """ Should add queryset and tb to the instance property """
        self.request_storage.add_queryset_instance(self.queryset, self.tb)
        self.assertIn(id(self.queryset), self.request_storage.queryset_stats)
        stats = self.request_storage.queryset_stats[id(self.queryset)]
        self.assertEqual(stats['queryset'], self.queryset)
        self.assertEqual(stats['tb'], self.tb)
        self.assertListEqual(stats['wrapped_model_instances'], [])

    def test_add_queryset_model_instance(self):
        """ Should add model instance to specified queryset stats dictionary """
        self.request_storage.add_queryset_instance(self.queryset, self.tb)
        model_instance_1 = Mock()
        model_instance_2 = Mock()
        self.request_storage.add_queryset_model_instance(self.queryset, model_instance_1)
        stats = self.request_storage.queryset_stats[id(self.queryset)]
        self.assertListEqual(stats['wrapped_model_instances'], [model_instance_1])
        self.request_storage.add_queryset_model_instance(self.queryset, model_instance_2)
        self.assertListEqual(stats['wrapped_model_instances'], [model_instance_1, model_instance_2])

    def test_recommendations_all_good(self):
        """ Should return corresponding message if all fields are good """
        used_fields = ['foo', 'bar']
        unused_fields = []
        recommendation = self.request_storage.get_defer_recommendations(used_fields, unused_fields)
        self.assertTrue(recommendation.startswith("Nothing to do here"))

    def test_recommendations_defer(self):
        """ Should return defer call example if there are more used fields """
        used_fields = ['foo', 'bar', 'Jake']
        unused_fields = ['spam', 'Finn']
        recommendation = self.request_storage.get_defer_recommendations(used_fields, unused_fields)
        self.assertEqual(recommendation, "Model.objects.defer('spam', 'Finn')")

    def test_recommendations_only(self):
        """ Should return only call example if there are more unused fields """
        used_fields = ['foo', 'bar']
        unused_fields = ['spam', 'Finn', 'Jake']
        recommendation = self.request_storage.get_defer_recommendations(used_fields, unused_fields)
        self.assertEqual(recommendation, "Model.objects.only('foo', 'bar')")

    def test_recommendations_no_fields_was_used(self):
        """ Should return corresponding message if no fields was used """
        used_fields = []
        unused_fields = ['spam', 'bar']
        recommendation = self.request_storage.get_defer_recommendations(used_fields, unused_fields)
        self.assertEqual(recommendation, "No fields were used. Consider to remove this request")
