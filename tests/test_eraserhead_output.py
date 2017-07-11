# encoding: utf-8
import sys
import re
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from django.test import TestCase, override_settings
from django.apps import apps
import term

from bar.models import Article


def capture_stdout(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        output = sys.stdout.read()
        sys.stdout = out
        return output
    finally:
        sys.stdout = out


def get_index_page(client, uri):
    resp = client.get(uri)


@override_settings(INSTALLED_APPS=('eraserhead.apps.EraserheadConfig', 'bar'), ERASERHEAD_ENABLED=True)
class EraserheadOutputTestCase(TestCase):

    """ Integration test """

    def setUp(self):
        super(EraserheadOutputTestCase, self).setUp()
        Article.objects.create(title='foobar', content=('spam ' * 10))
        Article.objects.create(title='barfoo', content=('spam ' * 10))

    def tearDown(self):
        super(EraserheadOutputTestCase, self).tearDown()
        apps.clear_cache()

    def test_eraserhead_output(self):
        """ Should display QuerySets information """
        output = term.strip(capture_stdout(get_index_page, self.client, '/'))
        self.assertIn("ERASERHEAD STATS", output)
        self.assertEqual(output.count("QuerySet #"), 2)
        # First QS
        self.assertIn('Instances created: 2\n', output)
        self.assertIn('Used fields: title\n', output)
        self.assertTrue(re.search('Unused\sfields\:\s(content|id),\s(content|id)\n', output))
        self.assertIn("Recommendations:  Model.objects.only('title')\n", output)
        self.assertIn('bar/views.py", line 7', output)
        self.assertIn('articles = list(Article.objects.all())', output)
        # Second QS
        self.assertIn('Instances created: 1\n', output)
        self.assertTrue(
            re.search('Used\sfields\:\s(content|id|title),\s(content|id|title),\s(content|id|title)\n', output))
        self.assertIn('Unused fields: \n', output)
        self.assertIn("Recommendations:  Nothing to do here ¯\_(ツ)_/¯\n", output)
        self.assertIn('bar/views.py", line 8', output)
        self.assertIn("article = Article.objects.get(title='foobar')", output)

    def test_output_nothing_if_no_querysets(self):
        """ Should not output anything if there are no QuerySets in request """
        output = term.strip(capture_stdout(get_index_page, self.client, '/empty'))
        self.assertNotIn("ERASERHEAD STATS", output)
