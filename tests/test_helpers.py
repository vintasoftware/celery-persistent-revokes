from unittest import TestCase
import mock
import six

from celery_persistent_revokes.helpers import (
    _get_revoke_backend, _is_task_scheduled, revoke, list_revokes, is_task_revoked,
    delete_revoke)


class GetRevokeBackendTests(TestCase):

    @mock.patch('celery_persistent_revokes.helpers.get_setting', return_value='test.module.path')
    @mock.patch('celery_persistent_revokes.helpers.import_class')
    def test_instances_backend_correctly(self, import_class, get_setting):
        backend_mock = mock.MagicMock()
        import_class.return_value = backend_mock

        _get_revoke_backend()

        get_setting.assert_called_once_with('CELERY_PERSISTENT_REVOKES_BACKEND')
        import_class.assert_called_once_with('test.module.path')

        backend_mock.assert_called_once_with()


class TaskIsScheduledTests(TestCase):

    @mock.patch('celery_persistent_revokes.helpers.inspect')
    def test_returns_true_if_task_is_scheduled(self, inspect):
        inspector_mock = mock.MagicMock()
        inspect.return_value = inspector_mock
        inspector_mock.scheduled = lambda: {
            'worker1.example.com': [
                {
                    "eta": "2010-06-07 09:07:52",
                    "priority": 0,
                    "request": {
                        "name": "tasks.sleeptask",
                        "id": "1a7980ea-8b19-413e-91d2-0b74f3844c4d",
                        "args": "[1]",
                        "kwargs": "{}"
                    }
                },
                {
                    "eta": "2010-06-07 09:07:53",
                    "priority": 0,
                    "request": {
                        "name": "tasks.sleeptask",
                        "id": "49661b9a-aa22-4120-94b7-9ee8031d219d",
                        "args": "[2]",
                        "kwargs": "{}"
                    }
                }
            ],
        }

        value_returned = _is_task_scheduled('1a7980ea-8b19-413e-91d2-0b74f3844c4d')

        self.assertTrue(value_returned)

    @mock.patch('celery_persistent_revokes.helpers.inspect')
    def test_returns_false_if_task_is_scheduled(self, inspect):
        inspector_mock = mock.MagicMock()
        inspect.return_value = inspector_mock
        inspector_mock.scheduled = lambda: {
            'worker1.example.com': [
                {
                    "eta": "2010-06-07 09:07:52",
                    "priority": 0,
                    "request": {
                        "name": "tasks.sleeptask",
                        "id": "1a7980ea-8b19-413e-91d2-0b74f3844c4d",
                        "args": "[1]",
                        "kwargs": "{}"
                    }
                },
                {
                    "eta": "2010-06-07 09:07:53",
                    "priority": 0,
                    "request": {
                        "name": "tasks.sleeptask",
                        "id": "49661b9a-aa22-4120-94b7-9ee8031d219d",
                        "args": "[2]",
                        "kwargs": "{}"
                    }
                }
            ],
        }

        value_returned = _is_task_scheduled('aloalo')

        self.assertFalse(value_returned)


class RevokeTests(TestCase):

    @mock.patch('celery_persistent_revokes.helpers._is_task_scheduled', return_value=True)
    @mock.patch('celery_persistent_revokes.helpers._get_revoke_backend')
    @mock.patch('celery_persistent_revokes.helpers.celery_revoke')
    def test_uses_backend_if_task_is_scheduled(
            self, celery_revoke, _get_revoke_backend, _is_task_scheduled):
        backend_mock = mock.MagicMock()
        _get_revoke_backend.return_value = backend_mock

        revoke('1a7980ea-8b19-413e-91d2-0b74f3844c4d')
        celery_revoke.assert_called_once_with('1a7980ea-8b19-413e-91d2-0b74f3844c4d')
        _get_revoke_backend.assert_called_once_with()
        backend_mock.revoke.assert_called_once_with('1a7980ea-8b19-413e-91d2-0b74f3844c4d')

    @mock.patch('celery_persistent_revokes.helpers._is_task_scheduled', return_value=False)
    @mock.patch('celery_persistent_revokes.helpers._get_revoke_backend')
    @mock.patch('celery_persistent_revokes.helpers.celery_revoke')
    def test_doesnt_use_backend_if_task_isnt_scheduled(
            self, celery_revoke, _get_revoke_backend, _is_task_scheduled):
        backend_mock = mock.MagicMock()
        _get_revoke_backend.return_value = backend_mock

        revoke('1a7980ea-8b19-413e-91d2-0b74f3844c4d')
        celery_revoke.assert_called_once_with('1a7980ea-8b19-413e-91d2-0b74f3844c4d')
        _get_revoke_backend.assert_not_called()
        backend_mock.revoke.assert_not_called()


class ListRevokesTests(TestCase):

    @mock.patch('celery_persistent_revokes.helpers._get_revoke_backend')
    def test_returns_same_result_as_the_backend(self, _get_revoke_backend):
        backend_mock = mock.MagicMock()
        _get_revoke_backend.return_value = backend_mock
        backend_mock.list_revokes = mock.Mock()
        backend_mock.list_revokes.return_value = ['a', 'b', 'c']

        value_returned = list_revokes()

        _get_revoke_backend.assert_called_once_with()
        backend_mock.list_revokes.assert_called_once_with()
        if six.PY2:
            self.assertItemsEqual(value_returned, ['a', 'b', 'c'])
        else:
            self.assertCountEqual(value_returned, ['a', 'b', 'c'])


class DeleteRevokeTests(TestCase):

    @mock.patch('celery_persistent_revokes.helpers._get_revoke_backend')
    def test_calls_backend_delete_revoke_method(self, _get_revoke_backend):
        backend_mock = mock.MagicMock()
        _get_revoke_backend.return_value = backend_mock

        delete_revoke('test-task')

        _get_revoke_backend.assert_called_once_with()
        backend_mock.delete_revoke.assert_called_once_with('test-task')


class IsTaskRevokedTests(TestCase):

    @mock.patch('celery_persistent_revokes.helpers._get_revoke_backend')
    def test_returns_true_if_backend_returns_true(self, _get_revoke_backend):
        backend_mock = mock.MagicMock()
        _get_revoke_backend.return_value = backend_mock
        backend_mock.is_task_revoked = mock.Mock()
        backend_mock.is_task_revoked.return_value = True

        value_returned = is_task_revoked('test-task')

        _get_revoke_backend.assert_called_once_with()
        backend_mock.is_task_revoked.assert_called_once_with('test-task')
        self.assertEqual(value_returned, True)

    @mock.patch('celery_persistent_revokes.helpers._get_revoke_backend')
    def test_returns_false_if_backend_returns_false(self, _get_revoke_backend):
        backend_mock = mock.MagicMock()
        _get_revoke_backend.return_value = backend_mock
        backend_mock.is_task_revoked = mock.Mock()
        backend_mock.is_task_revoked.return_value = False

        value_returned = is_task_revoked('test-task')

        _get_revoke_backend.assert_called_once_with()
        backend_mock.is_task_revoked.assert_called_once_with('test-task')
        self.assertEqual(value_returned, False)
