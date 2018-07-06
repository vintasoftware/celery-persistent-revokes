from unittest import TestCase
import mock
from model_mommy import mommy

from celery_persistent_revokes.models import CeleryTaskRevoke
from celery_persistent_revokes.decorators import revokable_task


class RevokableTaskDecoratorTests(TestCase):

    def test_function_not_called_if_task_is_revoked(self):
        original_function_mock = mock.MagicMock()

        def original_function(*args, **kwargs):
            return original_function_mock(*args, **kwargs)

        mocked_task = mock.MagicMock()
        mocked_task.request = mock.MagicMock()
        mocked_task.request.id = 'revoked-task-id'

        app = mock.MagicMock()
        app.task = (
            lambda *eargs, **ekwargs: (
                lambda f: (
                    lambda *args, **kwargs: f(mocked_task, *args, **kwargs)  # noqa
                )
            )
        )

        mommy.make(CeleryTaskRevoke, id='revoked-task-id')

        revokable_task(app)(original_function)()

        original_function_mock.assert_not_called()

    def test_function_called_if_task_isnt_revoked(self):
        original_function_mock = mock.MagicMock()

        def original_function(*args, **kwargs):
            return original_function_mock(*args, **kwargs)

        mocked_task = mock.MagicMock()
        mocked_task.request = mock.MagicMock()
        mocked_task.request.id = 'not-revoked-task-id'

        app = mock.MagicMock()
        app.task = (
            lambda *decorator_args, **decorator_kwargs: (
                lambda f: (
                    lambda *args, **kwargs: f(mocked_task, *args, **kwargs)  # noqa
                )
            )
        )
        revokable_task(app)(original_function)()

        original_function_mock.assert_called_once_with()

    def test_passes_self_to_function_if_bind_is_true(self):
        original_function_mock = mock.MagicMock()

        def original_function(*args, **kwargs):
            return original_function_mock(*args, **kwargs)

        mocked_task = mock.MagicMock()
        mocked_task.request = mock.MagicMock()
        mocked_task.request.id = 'revoked-task-id'

        app = mock.MagicMock()
        app.task = (
            lambda *decorator_args, **decorator_kwargs: (
                lambda f: (
                    lambda *args, **kwargs: f(mocked_task, *args, **kwargs)  # noqa
                )
            )
        )
        revokable_task(app, bind=True)(original_function)()

        original_function_mock.assert_called_once_with(mocked_task)

    def test_assigns_custom_task_name_to_task(self):
        original_function_mock = mock.MagicMock()

        def original_function(*args, **kwargs):
            return original_function_mock(*args, **kwargs)

        mocked_task = mock.Mock()
        mocked_task.request = mock.Mock()
        mocked_task.request.id = 'revoked-task-id'

        app = mock.MagicMock()
        revokable_task(app, name="my-custom-task-name")(original_function)()

        app.task.assert_called_once_with(bind=True, name='my-custom-task-name')
