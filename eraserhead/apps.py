from django.apps import AppConfig
from django.core.signals import request_started, request_finished

from .patch import request_started_handler, request_finished_handler, patch_queryset


class EraserheadConfig(AppConfig):
    name = 'eraserhead'

    def ready(self):
        patch_queryset()
        request_started.connect(request_started_handler)
        request_finished.connect(request_finished_handler)
