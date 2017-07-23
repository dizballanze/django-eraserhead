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
        deferred_fields = self.__wrapped__.get_deferred_fields()
        return {name for name, usage in self._fields.items() if (name not in deferred_fields) and (usage > 0)}

    @property
    def eraserhead_unused_fields(self):
        deferred_fields = self.__wrapped__.get_deferred_fields()
        return {name for name, usage in self._fields.items() if (name not in deferred_fields) and not usage}
