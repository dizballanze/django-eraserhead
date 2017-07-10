import wrapt


class ObjectWrapper(wrapt.ObjectProxy):

    _fields = {}

    def __init__(self, model_instance):
        super(ObjectWrapper, self).__init__(model_instance)
        self._fields = {f.name: 0 for f in model_instance._meta.fields}

    def __getattr__(self, name):
        if name in self._fields:
            self._fields[name] += 1
        return super(ObjectWrapper, self).__getattr__(name)

    def get_fields_usage(self):
        deferred_fields = self.__wrapped__.get_deferred_fields()
        return {k: v for k, v in self._fields.items() if k not in deferred_fields}
