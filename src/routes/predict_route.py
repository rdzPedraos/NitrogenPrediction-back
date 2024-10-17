from flask import request, jsonify

from . import main_blueprint
from utils.prediction import predict_nitrogen
from utils.session_manager import load_session_data

@main_blueprint.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    session_id = data.get('session_id')
    roi = data.get('roi')

    if not session_id or not roi:
        return jsonify({'error': 'Session ID or ROI not provided'}), 400

    session_data = load_session_data(session_id)
    if not session_data or session_data['status'] != 'processed':
        return jsonify({'error': 'Session not processed or invalid'}), 400

    result = predict_nitrogen(session_data, roi)
    if 'error' in result:
        return jsonify({'error': result['error']}), 500

    return jsonify(result), 200
