from celery.task.control import inspect, revoke as celery_revoke

from celery_persistent_revokes.utils import import_class
from celery_persistent_revokes.signals import (
    task_revoked, task_will_be_revoked, revoke_deleted, revoke_will_be_deleted)
from celery_persistent_revokes.settings import get_setting


def _get_revoke_backend():
    backend_path = get_setting('CELERY_PERSISTENT_REVOKES_BACKEND')
    backend_cls = import_class(backend_path)
    backend = backend_cls()
    return backend


def _is_task_scheduled(task_id):
    inspector = inspect()
    scheduled_tasks = inspector.scheduled()

    for worker_tasks in scheduled_tasks.values():
        for task in worker_tasks:
            if task_id == task['request']['id']:
                return True
    return False


def revoke(task_id, *args, **kwargs):
    celery_revoke(task_id, *args, **kwargs)

    if _is_task_scheduled(task_id):
        revoke_backend = _get_revoke_backend()
        task_will_be_revoked.send(sender=None, task_id=task_id)
        revoke_backend.revoke(task_id)
        task_revoked.send(sender=None, task_id=task_id)


def list_revokes():
    revoke_backend = _get_revoke_backend()
    return revoke_backend.list_revokes()


def is_task_revoked(task_id):
    revoke_backend = _get_revoke_backend()
    return revoke_backend.is_task_revoked(task_id)


def delete_revoke(task_id):
    revoke_backend = _get_revoke_backend()
    revoke_will_be_deleted.send(sender=None, task_id=task_id)
    revoke_backend.delete_revoke(task_id)
    revoke_deleted.send(sender=None, task_id=task_id)
