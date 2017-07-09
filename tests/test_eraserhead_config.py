from django.test import TestCase, override_settings
from django.apps import apps
from django.core.signals import request_started, request_finished


class EraserheadConfigTestCase(TestCase):

    def tearDown(self):
        apps.clear_cache()

    @override_settings(ERASERHEAD_ENABLED=False)
    def test_disabled_eraserhead(self):
        """ When eraserhead is disabled, request signals handlers shouldn't be connected """
        request_started_receivers_count_before = len(request_started.receivers)
        request_finished_receivers_count_before = len(request_finished.receivers)
        with override_settings(INSTALLED_APPS=("eraserhead.apps.EraserheadConfig",)):
            apps.get_app_config('eraserhead')
        self.assertEqual(request_started_receivers_count_before, len(request_started.receivers))
        self.assertEqual(request_finished_receivers_count_before, len(request_finished.receivers))

    @override_settings(ERASERHEAD_ENABLED=True)
    def test_enbaled_eraserhead(self):
        """ When eraserhead is enabled, request signals handlers should be connected """
        request_started_receivers_count_before = len(request_started.receivers)
        request_finished_receivers_count_before = len(request_finished.receivers)
        with override_settings(INSTALLED_APPS=("eraserhead.apps.EraserheadConfig",)):
            apps.get_app_config('eraserhead')
        self.assertEqual(request_started_receivers_count_before + 1, len(request_started.receivers))
        self.assertEqual(request_finished_receivers_count_before + 1, len(request_finished.receivers))
