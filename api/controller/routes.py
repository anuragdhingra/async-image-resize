from flask import jsonify, Blueprint, request
from api.controller import tasks
import logging
import uuid


bp = Blueprint('tasks', __name__)
logger = logging.getLogger()


@bp.route('/resize', methods=['POST'])
def resize_image():
    img_string = request.json['imageData']
    new_file_uuid = str(uuid.uuid4())
    task = tasks.async_resize.delay(new_file_uuid, img_string)

    return jsonify({
        'success': True,
        'token': task.id,
    }), 202


@bp.route('/status', methods=['GET'])
def get_status():
    task_id = request.json['token']
    state = tasks.check_status(task_id)
    return jsonify({
        'status': state.get('status'),
        'resized_image_url': state.get('info'),
    }), 200
