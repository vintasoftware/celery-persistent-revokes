import django.dispatch


task_revoked = django.dispatch.Signal(providing_args=["task_id"])
task_will_be_revoked = django.dispatch.Signal(providing_args=["task_id"])
revoke_deleted = django.dispatch.Signal(providing_args=["task_id"])
revoke_will_be_deleted = django.dispatch.Signal(providing_args=["task_id"])
