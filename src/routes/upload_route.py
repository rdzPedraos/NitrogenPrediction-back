import uuid
from flask import request, jsonify
from utils.file_manager import saveBandFile, FILE_TYPES

from . import main_blueprint

@main_blueprint.route('/upload-images', methods=['POST'])
def upload_images():
    files = request.files

    if(FILE_TYPES['BANDS'] not in files or FILE_TYPES['PANELS'] not in files):
        return jsonify({'message': 'Invalid files'}), 400

    session_id = str(uuid.uuid4())

    # Guardar archivos subidos
    for type in FILE_TYPES.values():
        for i, file in enumerate(files.getlist(type)):
            saveBandFile(file, session_id, type, i)

    return jsonify({'session_id': session_id}), 200
