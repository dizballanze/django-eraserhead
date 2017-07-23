import sys

import wrapt


class ModelInstanceWrapper(wrapt.ObjectProxy):

    _fields = {}

    def __init__(self, model_instance):
        super(ModelInstanceWrapper, self).__init__(model_instance)
        self._fields = {f.name: 0 for f in model_instance._meta.fields}

    def __getattr__(self, name):
        if name in self._fields:
            self._fields[name] += 1
        return super(ModelInstanceWrapper, self).__getattr__(name)

    # Long methods names to avoid collisions with model instance method names

    @property
    def eraserhead_used_fields(self):
        return self._eraserhead_filtered_fields_list(lambda usage: usage > 0)

    @property
    def eraserhead_unused_fields(self):
        return self._eraserhead_filtered_fields_list(lambda usage: not usage)

    @property
    def eraserhead_unused_fields_size(self):
        total_size = 0
        for field in self.eraserhead_unused_fields:
            total_size += sys.getsizeof(getattr(self.__wrapped__, field))
        return total_size

    def _eraserhead_filtered_fields_list(self, condition):
        deferred_fields = self.__wrapped__.get_deferred_fields()
        return {name for name, usage in self._fields.items() if (name not in deferred_fields) and condition(usage)}
