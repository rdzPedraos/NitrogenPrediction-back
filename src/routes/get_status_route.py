import os
from flask import request, jsonify
from . import main_blueprint

from utils.FileManager import listFiles
from utils.ImageGenerator import ImageGenerator

@main_blueprint.route('/<session_id>/status', methods=['GET'])
def get_status(session_id):
    images = [file.name for file in listFiles(session_id, 'images')]

    # Obtener la lista de índices y sus etiquetas
    info = []

    for key, label in ImageGenerator.FILTERS_KEY.items():
        filename = f'{key}.png'
        status = filename in images

        info.append({
            'label': label,
            'key': key,
            'status': status
        })

    return jsonify(info), 200
