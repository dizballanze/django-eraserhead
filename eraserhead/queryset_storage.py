# encoding: utf-8
import traceback

from django.conf import settings
import term


class QuerySetStorage(object):

    """ Store statistics about single QuerySet """

    def __init__(self, queryset, traceback):
        self._queryset = queryset
        self._traceback = traceback
        self._wrapped_model_instances = []

    def add_wrapped_model_instance(self, wrapped_model_instance):
        self._wrapped_model_instances.append(wrapped_model_instance)

    @property
    def instances_count(self):
        return len(self._wrapped_model_instances)

    @property
    def model_name(self):
        return self._queryset.model()._meta.object_name
    
    @property
    def queryset_id(self):
        return id(self._queryset)

    def get_defer_recommendations(self, used_fields, unused_fields):
        if not len(used_fields):
            return 'No fields were used. Consider to remove this request'
        if not len(unused_fields):
            return 'Nothing to do here ¯\_(ツ)_/¯'
        if len(used_fields) > len(unused_fields):
            func = 'defer'
            fields = unused_fields
        else:
            func = 'only'
            fields = used_fields
        quoted_fields = ["'{}'".format(field) for field in fields]
        return 'Model.objects.{}({})'.format(func, ', '.join(quoted_fields))

    def print_stats(self):
        term.writeLine("\n\tQuerySet #{}".format(self.queryset_id), term.bold)
        self._print_named_value("Instances created", self.instances_count)
        self._print_named_value("Model", self.model_name)
        self._print_fields_usage(self._wrapped_model_instances)
        self._print_traceback()

    def _print_traceback(self):
        base_path = getattr(settings, 'ERASERHEAD_TRACEBACK_BASE_PATH', None)
        for trace_line in traceback.format_list(self._traceback):
            if base_path and (base_path not in trace_line):
                continue
            print("\t" + trace_line.strip().replace('\n', '\n\t'))

    def _print_fields_usage(self, wrapped_model_instances):
        used_fields = set()
        all_fields = set()
        for instance in wrapped_model_instances:
            used_fields = used_fields | instance.eraserhead_used_fields
            all_fields = instance.eraserhead_used_fields | instance.eraserhead_unused_fields
        unused_fields = all_fields - used_fields
        self._print_named_value('Used fields', ', '.join(used_fields))
        self._print_named_value('Unused fields', ', '.join(unused_fields))
        self._print_named_value(
            'Recommendations', term.format(self.get_defer_recommendations(used_fields, unused_fields), term.reverse))

    def _print_named_value(self, label, value):
        term.write('\t')
        term.write(label + ':', term.underscore)
        term.writeLine(" {}".format(value))
