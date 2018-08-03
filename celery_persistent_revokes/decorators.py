from celery.utils.log import get_task_logger
from celery_persistent_revokes.helpers import is_task_revoked, delete_revoke

logger = get_task_logger(__name__)


def revokable_task(app, *args, **kwargs):
    def revokable_task_decorator(func):
        original_task_has_bind = kwargs.get('bind', False)
        original_func_path = '{}.{}'.format(func.__module__, func.__name__)

        kwargs['bind'] = True
        kwargs['name'] = kwargs.get('name', original_func_path)

        @app.task(*args, **kwargs)
        def func_wrapper(self, *task_args, **task_kwargs):
            task_id = self.request.id
            if is_task_revoked(task_id):
                delete_revoke(task_id)
                logger.warning(
                    'Task {} was revoked by celery_persistent_revokes successfully'.format(task_id))
                return None

            if original_task_has_bind:
                return func(self, *task_args, **task_kwargs)

            return func(*task_args, **task_kwargs)

        return func_wrapper

    return revokable_task_decorator
