from django.contrib import admin
from celery_persistent_revokes.settings import get_setting
from celery_persistent_revokes.models import CeleryTaskRevoke


if (get_setting('CELERY_PERSISTENT_REVOKES_BACKEND') ==
        'celery_persistent_revokes.backends.DjangoDatabase'):
    admin.site.register(CeleryTaskRevoke)
