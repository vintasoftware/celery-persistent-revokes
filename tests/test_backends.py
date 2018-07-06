from unittest import TestCase
import six
from model_mommy import mommy
from django.test import override_settings

from celery_persistent_revokes.backends import DjangoDatabase
from celery_persistent_revokes.models import CeleryTaskRevoke


class DjangoDatabaseTests(TestCase):

    def setUp(self):
        self.backend = DjangoDatabase()
        CeleryTaskRevoke.objects.all().delete()

    def tests_revokes_correctly(self):
        self.backend.revoke('test-task')
        self.assertIsNotNone(CeleryTaskRevoke.objects.filter(id='test-task').first())

    def tests_list_revokes_correctly(self):
        revokes = mommy.make(CeleryTaskRevoke, _quantity=10)
        revokes_ids = [r.id for r in revokes]
        listed_revoked_task_ids = self.backend.list_revokes()

        if six.PY2:
            self.assertItemsEqual(revokes_ids, listed_revoked_task_ids)
        else:
            self.assertCountEqual(revokes_ids, listed_revoked_task_ids)

    def tests_delete_revoke_correctly(self):
        revoke = mommy.make(CeleryTaskRevoke)
        revoke_id = revoke.id
        self.backend.delete_revoke(revoke_id)
        self.assertIsNone(CeleryTaskRevoke.objects.filter(id=revoke_id).first())

    def tests_returns_if_task_is_revoked_correctly(self):
        revoke = mommy.make(CeleryTaskRevoke)
        revoke_id = revoke.id
        self.assertTrue(self.backend.is_task_revoked(revoke_id))
        self.assertFalse(self.backend.is_task_revoked('not-revoked-task'))

    @override_settings(
        CELERY_PERSISTENT_REVOKES_MODEL='celery_persistent_revokes.CeleryTaskRevoke')
    def tests_gets_the_revoke_model_correctly(self):
        retrieved_model = self.backend._get_revoke_model()  # noqa
        self.assertEqual(retrieved_model, CeleryTaskRevoke)
