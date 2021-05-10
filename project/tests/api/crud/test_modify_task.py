import unittest

from mongoengine import connect, disconnect

from app.api import crud
from app.models.mongo import Task


class TestModifyTask(unittest.TestCase):

    def setUp(self):
        connect("mongoenginetest", host="mongomock://localhost")

    def tearDown(self):
        disconnect()

    def test_modify_task_success(self):
        expected_output = "test result"
        task_created = Task(command=expected_output)
        task_created.save()
        assert task_created
        crud.modify_task(str(task_created.pk), expected_output)
        task_modified = Task.objects.get(id=task_created.pk)
        assert task_modified.output == expected_output
        assert task_modified.started
    
    def test_modify_task_fails(self):
        self.tearDown()
        task_modified = crud.modify_task("", "")
        assert not task_modified
