# encoding: utf-8
import traceback

from django.conf import settings
import term
import humanfriendly


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

    @property
    def total_used_fields(self):
        used_fields = set()
        for wrapped_instance in self._wrapped_model_instances:
            used_fields |= wrapped_instance.eraserhead_used_fields
        return used_fields

    @property
    def total_unused_fields(self):
        unused_fields = None
        for wrapped_instance in self._wrapped_model_instances:
            if unused_fields is None:
                unused_fields = wrapped_instance.eraserhead_unused_fields
                continue
            unused_fields &= wrapped_instance.eraserhead_unused_fields
        return unused_fields or set()

    @property
    def total_wasted_memory(self):
        wasted_memory = 0
        for wrapped_instance in self._wrapped_model_instances:
            wasted_memory += wrapped_instance.eraserhead_unused_fields_size
        return wasted_memory

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
        self._print_named_value('Used fields', ', '.join(self.total_used_fields))
        self._print_named_value('Unused fields', ', '.join(self.total_unused_fields))
        self._print_named_value('Wasted memory', humanfriendly.format_size(self.total_wasted_memory))
        self._print_named_value(
            'Recommendations', term.format(
                self.get_defer_recommendations(self.total_used_fields, self.total_unused_fields), term.reverse))

    def _print_named_value(self, label, value):
        term.write('\t')
        term.write(label + ':', term.underscore)
        term.writeLine(" {}".format(value))
