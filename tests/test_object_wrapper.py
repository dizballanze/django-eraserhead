import sys
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from django.test import TestCase

from eraserhead.model_instance_wrapper import ModelInstanceWrapper


class ModelInstanceWrapperTestCase(TestCase):

    def setUp(self):
        super(ModelInstanceWrapperTestCase, self).setUp()
        meta_mock = Mock()
        meta_mock.fields = []
        for i in range(1, 5):
            field_mock = Mock()
            field_mock.name = 'field{}'.format(i)
            meta_mock.fields.append(field_mock)
        model_instance_mock = Mock()
        model_instance_mock._meta = meta_mock
        model_instance_mock.get_deferred_fields = Mock(return_value=[])
        self.model_instance_mock = model_instance_mock
        self.wrapper = ModelInstanceWrapper(model_instance_mock)

    def test_used_fields(self):
        """ Should return correct used fields list """
        self.wrapper.field1
        self.wrapper.field3
        self.assertEqual(set(self.wrapper.eraserhead_used_fields), {'field1', 'field3'})

    def test_unused_fields(self):
        """ Should return correct unused fields list """
        self.wrapper.field1
        self.wrapper.field3
        self.assertEqual(set(self.wrapper.eraserhead_unused_fields), {'field2', 'field4'})

    def test_should_not_return_deferred_fields(self):
        self.wrapper.field1
        self.wrapper.field3
        self.model_instance_mock.get_deferred_fields = Mock(return_value=['field2'])
        self.assertEqual(set(self.wrapper.eraserhead_unused_fields), {'field4'})

    def test_should_not_track_non_field_properties_of_instance(self):
        self.wrapper.field1
        self.wrapper.field3
        self.wrapper.not_a_field
        self.assertEqual(set(self.wrapper.eraserhead_used_fields), {'field1', 'field3'})

    def test_unused_fields_size(self):
        """ Should return correct size of unused fields values """
        self.model_instance_mock.field2 = 'foobar'
        self.model_instance_mock.field4 = 'spam' * 10
        expected_size = sys.getsizeof('foobar') + sys.getsizeof('spam' * 10)
        self.wrapper.field1
        self.wrapper.field3
        self.assertEqual(self.wrapper.eraserhead_unused_fields_size, expected_size)
