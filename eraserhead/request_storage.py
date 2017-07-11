# encoding: utf-8
from __future__ import print_function
from collections import OrderedDict
import traceback

from django.conf import settings
import term


class RequestStorage(object):

    """ Stores statistics about single request """

    def __init__(self):
        self.queryset_stats = OrderedDict()

    def add_queryset_instance(self, queryset, tb):
        queryset_id = id(queryset)
        self.queryset_stats[queryset_id] = {
            'queryset': queryset, 'tb': tb, 'wrapped_model_instances': []}

    def add_queryset_model_instance(self, queryset, wrapped_instance):
        self.queryset_stats[id(queryset)]['wrapped_model_instances'].append(wrapped_instance)

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

    # Stats print methods

    def print_stats(self):
        """ Display statistics of current request """
        if not self.queryset_stats:
            return
        term.writeLine("\n\t ERASERHEAD STATS \n", term.bold, term.reverse)
        for _, queryset_stats in self.queryset_stats.items():
            self._print_queryset_usage(
                queryset_stats['queryset'], queryset_stats['tb'], queryset_stats['wrapped_model_instances'])
        print()

    def _print_queryset_usage(self, queryset, tb, wrapped_model_instances):
        term.writeLine("\n\tQuerySet #{}".format(id(queryset)), term.bold)
        self._print_named_value("Instances created", len(wrapped_model_instances))
        self._print_named_value("Model", queryset.model()._meta.object_name)
        self._print_fields_usage(wrapped_model_instances)
        self._print_traceback(tb)

    def _print_traceback(self, tb):
        for trace_line in traceback.format_list(tb):
            if hasattr(settings, 'BASE_DIR') and (settings.BASE_DIR not in trace_line):
                continue
            print("\t" + trace_line.strip().replace('\n', '\n\t'), end="\n")

    def _print_fields_usage(self, wrapped_model_instances):
        fields = {}
        for instance in wrapped_model_instances:
            for field_name, usage in instance.get_fields_usage().items():
                if field_name not in fields:
                    fields[field_name] = 0
                fields[field_name] += usage
        sorted_fields = sorted(fields.items(), key=lambda i: i[1], reverse=True)
        used_fields = [f[0] for f in sorted_fields if f[1] > 0]
        unused_fields = [f[0] for f in sorted_fields if not f[1]]
        self._print_named_value('Used fields', ', '.join(used_fields))
        self._print_named_value('Unused fields', ', '.join(unused_fields))
        self._print_named_value(
            'Recommendations', term.format(self.get_defer_recommendations(used_fields, unused_fields), term.reverse))

    def _print_named_value(self, label, value):
        term.write('\t')
        term.write(label + ':', term.underscore)
        term.writeLine(" {}".format(value))
