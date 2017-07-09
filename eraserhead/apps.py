from django.apps import AppConfig
from django.conf import settings
from django.core.signals import request_started, request_finished

from eraserhead.patch import request_started_handler, request_finished_handler, patch_queryset


class EraserheadConfig(AppConfig):
    name = 'eraserhead'

    def ready(self):
        if getattr(settings, 'ERASERHEAD_ENABLED', False):
            patch_queryset()
            request_started.connect(request_started_handler)
            request_finished.connect(request_finished_handler)
