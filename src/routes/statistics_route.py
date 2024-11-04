from flask import request, jsonify
from utils.FileManager import getFilePath, getCoordinatesFromPercentage
from utils.ImageGenerator import ImageGenerator
from utils.ImagePredictor import ImagePredictor
from . import main_blueprint


requierd_roi = ['x', 'y', 'width', 'height']

@main_blueprint.route('/<session_id>/get-statistics', methods=['POST'])
def statistics(session_id):
    roi_coordinates = request.json.get('roi') 
    index = request.json.get('band')

    if not roi_coordinates or not all(key in roi_coordinates for key in requierd_roi):
        return jsonify({'error': 'Missing keys in roi_coordinates'}), 400

    if index not in ImageGenerator.FILTERS_KEY:
        return jsonify({'error': 'Index not found'}),

    # Convertir el % del ROI a píxeles
    defaultImage = getFilePath(session_id, 'rgb.png', 'images')
    roi_coordinates = getCoordinatesFromPercentage(defaultImage, roi_coordinates)

    # Crear una instancia de ImageGenerator y cargar los índices
    generator = ImageGenerator(None, session_id)  # No necesitamos el processor en este caso
    generator.load_indices()

    predictor = ImagePredictor(generator)
    predictor.set_roi(roi_coordinates)
    statistics = predictor.compute_statistics(index)

    return jsonify(statistics), 200
