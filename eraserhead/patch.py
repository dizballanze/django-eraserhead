import traceback

from django.db.models import query
import funcy

from .object_wrapper import ObjectWrapper
from .request_storage import RequestStorage


current_request_storage = RequestStorage()


@funcy.once
def patch_queryset():
    """ Patch QuerySet """

    # Patch `ModelIterable.__iter__` method
    @funcy.monkey(query.ModelIterable)
    def __iter__(self):
        tb = traceback.extract_stack()
        current_request_storage.add_queryset_instance(self.queryset, tb)
        iterator = __iter__.original(self)
        for model_instance in iterator:
            wrapped_model_instance = ObjectWrapper(model_instance)
            current_request_storage.add_queryset_model_instance(self.queryset, wrapped_model_instance)
            yield wrapped_model_instance


def request_started_handler(sender, **kwargs):
    """ Create new request storage """
    global current_request_storage
    current_request_storage = RequestStorage()


def request_finished_handler(sender, **kwargs):
    """ Print request statistics """
    current_request_storage.print_stats()
