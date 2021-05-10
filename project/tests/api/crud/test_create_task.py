import unittest

from mongoengine import connect, disconnect

from app.api import crud


class TestCreateTask(unittest.TestCase):

    def setUp(self):
        connect("mongoenginetest", host="mongomock://localhost")

    def tearDown(self):
        disconnect()

    def test_create_task_success(self):
        task_created = crud.create_task({"cmd":"ls"})
        assert task_created
        assert isinstance(task_created, tuple)
        assert task_created[0].get("id")
        assert not task_created[1]

    def test_create_task_fails(self):
        self.tearDown()
        task_not_created = crud.create_task({"cmd":"ls"})
        assert task_not_created
        assert isinstance(task_not_created, tuple)
        assert task_not_created[0].get("msg")
        assert task_not_created[1]
