import unittest

from mongoengine import connect, disconnect

from app.models.mongo import Task


class TestTaskModel(unittest.TestCase):

    @classmethod
    def setUp(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
       disconnect()

    def test_create(self):
        task = Task(command='ls')
        task.save()
        task_created = Task.objects().first()
        assert task_created
        assert task_created.command ==  'ls'
