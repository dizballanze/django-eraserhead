# encoding: utf-8
from __future__ import print_function

import term
import humanfriendly


class RequestStorage(object):

    """ Stores statistics about single request """

    def __init__(self):
        self.queryset_stats = []

    def add_queryset_storage_instance(self, queryset_storage):
        self.queryset_stats.append(queryset_storage)

    @property
    def total_wasted_memory(self):
        wasted_memory = 0
        for qs_storage in self.queryset_stats:
            wasted_memory += qs_storage.total_wasted_memory
        return wasted_memory

    # Stats print methods

    def print_stats(self):
        """ Display statistics of current request """
        if not self.queryset_stats:
            return
        term.writeLine("\n\t ERASERHEAD STATS \n", term.bold, term.reverse)
        for queryset_storage in self.queryset_stats:
            queryset_storage.print_stats()
        print()
        term.write("\t TOTAL WASTED MEMORY: ", term.bold, term.reverse)
        term.write("  {}".format(humanfriendly.format_size(self.total_wasted_memory)), term.red)
        print()
