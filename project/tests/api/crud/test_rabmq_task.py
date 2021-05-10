import os
import unittest
from unittest import mock

from mongoengine import connect, disconnect

from app.api import crud
from app.models.mongo import Task


class TestRabMQTask(unittest.TestCase):

    def test_rabbmq_task(self):
        
        with mock.patch("app.api.crud.modify_task") as modify_task_mock:
            modify_task_mock.return_value = True
            with mock.patch("app.api.crud.os") as os_mock:
                os_mock.popen = mock.MagicMock()
                body = '{"cmd": "cd", "task_id": "T3st_1d"}'
                crud.rabmq_task(body)
                assert os_mock.popen.call_args == mock.call("cd")
