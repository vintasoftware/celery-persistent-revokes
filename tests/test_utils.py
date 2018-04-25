from unittest import TestCase

from celery_persistent_revokes.utils import import_class
from celery_persistent_revokes.backends import DjangoDatabase


class ImportClassTests(TestCase):

    def test_import_class_correctly(self):
        imported_cls = import_class('celery_persistent_revokes.backends.DjangoDatabase')
        self.assertEqual(imported_cls, DjangoDatabase)
