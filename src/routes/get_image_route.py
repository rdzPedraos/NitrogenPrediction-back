from flask import send_file, jsonify
import os

from . import main_blueprint
from utils.session_manager import load_session_data

@main_blueprint.route('/images/<session_id>/<image_type>', methods=['GET'])
def get_processed_image(session_id, image_type):
    session_data = load_session_data(session_id)
    if not session_data:
        return jsonify({'error': 'Session not found'}), 404

    image_path = session_data['images'].get(image_type)
    if not image_path or not os.path.exists(image_path):
        return jsonify({'error': 'Image not found'}), 404

    return send_file(image_path, mimetype='image/png')
