import json
import logging
import os
import random

from app.main import ramq
from app.models.mongo import Task


logger = logging.Logger(name="logger", level=40)

def create_task(task_data: dict) -> tuple:
    """Creates a new object within mongo db and returns its ID.

    Args:
        task_data (dict): contains the command to execute.

    Returns:
        dict: contains the object's ID created. 
    """
    command = task_data.get("cmd")
    try:
        task_created = Task(command=command).save()
        task_id = str(task_created.pk)
        ramq.send({
                "message_id": random.randint(10000, 99999),
                "cmd": command,
                "task_id": task_id
            },
            routing_key='flask_rabmq.task',
            exchange_name='flask_rabmq'
        )
        return {"id": task_id}, False
    except Exception as e:
        logger.error(f"Error saving task on mongo: {e}")
        return {"msg": "It wasn't possible to create task."}, True


def get_task(task_id: str) -> dict:
    try:
        existing_task = Task.objects.get(id=task_id)
        if existing_task:
            result = {
                "id": str(existing_task.pk),
                "started": existing_task.started,
                "output": existing_task.output
            }
            return result, False
    except Exception as e:
        logger.error(f"Error getting task from mongo: {e}")
        return {"msg": f"Does not exist object {task_id}"}, True


def modify_task(task_id: str, output: str) -> bool:
    """ Modifies an object by task_id adding output.

    Args:
        task_id (int): Task ID object.
        output (str): result from command executed.

    Returns:
        bool: if task was modified returns True otherwise False.
    """
    try:
        existing_task = Task.objects.get(id=task_id)
        if existing_task:
            existing_task.output = output
            existing_task.started = True
            existing_task.save()
            return True
    except Exception as e:
        logger.error(f"Error modifiying task on mongo: {e}")
        return False


@ramq.queue(exchange_name='flask_rabmq', routing_key='flask_rabmq.task')
def rabmq_task(body: str) -> bool:
    """Background task executed on rabbit queue.

    Args:
        body (str): data to execute task.

    Returns:
        bool: returns result from modify_task method.
    """
    body = json.loads(body)
    cmd = body.get("cmd")
    task_id = body.get("task_id")
    from unittest import mock
    cmd_output = os.popen(f"{cmd}").read()
    return modify_task(task_id, cmd_output)
