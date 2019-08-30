from flask import Flask, jsonify, Blueprint, request, abort
from api.controller import tasks
import logging
import uuid


bp = Blueprint('tasks', __name__)
logger = logging.getLogger()

@bp.route('/resize', methods=['POST'])
def resize_image():
    img_string = request.json['imageData']
    new_file_uuid = str(uuid.uuid4())
    tasks.async_resize.delay(new_file_uuid,img_string)

    return jsonify({
        'success': True,
        'token': new_file_uuid,
    }), 202