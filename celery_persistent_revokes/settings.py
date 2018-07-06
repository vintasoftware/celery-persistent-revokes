import os

is_django_available = True
try:
    from django.conf import settings
except ImportError:
    is_django_available = False


DEFAULT_SETTINGS = {
    'CELERY_PERSISTENT_REVOKES_BACKEND':
        'celery_persistent_revokes.backends.DjangoDatabase',
    'CELERY_PERSISTENT_REVOKES_MODEL': 'celery_persistent_revokes.CeleryTaskRevoke',
}


def get_setting(setting_key):
    env_value = os.environ.get(setting_key, None)

    django_settings_value = None
    if is_django_available:
        django_settings_value = getattr(settings, setting_key, None)

    return env_value or django_settings_value or DEFAULT_SETTINGS.get(setting_key)
