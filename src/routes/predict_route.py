from flask import request, jsonify
from utils.ImageGenerator import ImageGenerator
from utils.ImagePredictor import ImagePredictor
from . import main_blueprint


requierd_roi = ['x', 'y', 'width', 'height']
required_iot = ['soil_humedity', 'soil_temperature', "pH", "avg_spad"]

@main_blueprint.route('/<session_id>/predict', methods=['POST'])
def predict(session_id):
    roi_coordinates = request.json.get('roi_coordinates') 
    data_iot = request.json.get('data_iot')

    if not data_iot or not all(key in data_iot for key in required_iot):
        return jsonify({'error': 'Missing keys in data_iot'}), 400
    
    if not roi_coordinates or not all(key in roi_coordinates for key in requierd_roi):
        return jsonify({'error': 'Missing keys in roi_coordinates'}), 400
    
    # Crear una instancia de ImageGenerator y cargar los índices
    generator = ImageGenerator(None, session_id)  # No necesitamos el processor en este caso
    generator.load_indices()

    predictor = ImagePredictor(generator)
    predictor.set_roi(roi_coordinates)
    predictor.compute_statistics()
    prediction = predictor.predict(data_iot)

    return jsonify(str(prediction)), 200
