
from celery_persistent_revokes.settings import get_setting


class DjangoDatabase(object):

    def __init__(self):
        self.revoke_model = self._get_revoke_model()

    def _get_revoke_model(self):
        from django.apps import apps
        from django.core.exceptions import ImproperlyConfigured

        try:
            model_app, model_name = get_setting('CELERY_PERSISTENT_REVOKES_MODEL').split('.')
        except ValueError:
            raise ImproperlyConfigured(
                "`CELERY_PERSISTENT_REVOKES_MODEL` should be in format "
                "<app_name>.<ModelName>")

        return apps.get_model(model_app, model_name)

    def revoke(self, task_id):
        self.revoke_model.objects.create(pk=task_id)

    def list_revokes(self):
        return self.revoke_model.objects.all().values_list('pk', flat=True).iterator()

    def is_task_revoked(self, task_id):
        from django.core.exceptions import ObjectDoesNotExist
        try:
            return self.revoke_model.objects.get(pk=task_id)
        except ObjectDoesNotExist:
            return None

    def delete_revoke(self, task_id):
        self.revoke_model.objects.filter(pk=task_id).delete()
