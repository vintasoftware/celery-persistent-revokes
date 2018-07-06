from unittest import TestCase
import six
from django.test import override_settings

from celery_persistent_revokes.settings import get_setting

if six.PY2:
    # Python(2.7 < 3)
    from test.test_support import EnvironmentVarGuard  # noqa
else:
    # Python >=3
    from test.support import EnvironmentVarGuard  # noqa


class GetSettingsTests(TestCase):

    @override_settings(CELERY_PERSISTENT_REVOKES_BACKEND='test.a.b')
    def test_get_django_setting_present(self):
        self.assertEqual('test.a.b', get_setting('CELERY_PERSISTENT_REVOKES_BACKEND'))

    def test_get_django_settings_missing(self):
        self.assertEqual(
            'celery_persistent_revokes.backends.DjangoDatabase',
            get_setting('CELERY_PERSISTENT_REVOKES_BACKEND'))

    def test_get_env_var(self):
        env = EnvironmentVarGuard()
        env.set('CELERY_PERSISTENT_REVOKES_BACKEND', 'test.a.b')
        with env:
            setting_value = get_setting('CELERY_PERSISTENT_REVOKES_BACKEND')
        self.assertEqual(setting_value, 'test.a.b')

    @override_settings(CELERY_PERSISTENT_REVOKES_BACKEND='test.a.b')
    def test_get_django_settings_with_env_var_set(self):
        env = EnvironmentVarGuard()
        env.set('CELERY_PERSISTENT_REVOKES_BACKEND', 'test.env')
        with env:
            setting_value = get_setting('CELERY_PERSISTENT_REVOKES_BACKEND')
        self.assertEqual(setting_value, 'test.env')

    def test_get_django_setting_and_env_var_missing(self):
        setting_value = get_setting('CELERY_PERSISTENT_REVOKES_BACKEND')
        self.assertEqual(
            setting_value, 'celery_persistent_revokes.backends.DjangoDatabase')
