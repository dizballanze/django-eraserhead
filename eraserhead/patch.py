import traceback

from django.db.models import query
import funcy

from eraserhead.model_instance_wrapper import ModelInstanceWrapper
from eraserhead.request_storage import RequestStorage
from eraserhead.queryset_storage import QuerySetStorage


current_request_storage = RequestStorage()


@funcy.once
def patch_queryset():
    """ Patch QuerySet """

    # Patch `ModelIterable.__iter__` method
    @funcy.monkey(query.ModelIterable)
    def __iter__(self):
        tb = traceback.extract_stack()
        queryset_storage = QuerySetStorage(self.queryset, tb)
        current_request_storage.add_queryset_storage_instance(queryset_storage)
        iterator = __iter__.original(self)
        for model_instance in iterator:
            wrapped_model_instance = ModelInstanceWrapper(model_instance)
            queryset_storage.add_wrapped_model_instance(wrapped_model_instance)
            yield wrapped_model_instance


def request_started_handler(sender, **kwargs):
    """ Create new request storage """
    global current_request_storage
    current_request_storage = RequestStorage()


def request_finished_handler(sender, **kwargs):
    """ Print request statistics """
    current_request_storage.print_stats()
