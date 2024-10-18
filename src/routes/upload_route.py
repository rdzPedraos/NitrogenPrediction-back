import uuid
from flask import request, jsonify
from utils.file_manager import save

from . import main_blueprint

@main_blueprint.route('/upload-images', methods=['POST'])
def upload_images():
    if "bands" not in request.files or "panels" not in request.files:
        return jsonify({'message': 'Invalid request'}), 400

    session_id = str(uuid.uuid4())
    bands = request.files.getlist('bands')
    panels = request.files.getlist('panels')

    # Guardar archivos subidos
    for files, key in zip([bands, panels], ['bands', 'panels']):
        for id in range(len(files)):
            save(session_id, files[id], f"{key}_{str(id+1)}.tif")

    return jsonify({'session_id': session_id}), 200
