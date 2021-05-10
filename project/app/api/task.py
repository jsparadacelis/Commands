from flask import Blueprint, request, jsonify

from app.api import crud


task_bp = Blueprint("task", __name__, url_prefix="/task")

@task_bp.route("/", methods=["POST"])
@task_bp.route("/<task_id>", methods=["GET"])
def task_endpoint(task_id: str = None) -> tuple:
    """ Endpoint that receives GET and POST http requests.
    Args:
        task_id (str, optional): [description]. Defaults to None.

    Returns:
        [tuple]: returns http response and http code.
    """
    if request.method == "POST":
        task_data = request.json
        task_info, error = crud.create_task(task_data)
        http_status = 400 if error else 201 
        return jsonify(task_info), http_status
    
    if request.method == "GET":
        task_info, error = crud.get_task(task_id)
        http_status = 404 if error else 200 
        return jsonify(task_info), http_status
