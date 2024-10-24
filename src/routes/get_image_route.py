import os
from flask import send_file, abort

from . import main_blueprint
from utils.ImageGenerator import ImageGenerator
from utils.FileManager import getFilePath

@main_blueprint.route('/<session_id>/<folder>/<band_key>', methods=['GET'])
def get_processed_image(session_id, folder, band_key):
    if band_key not in ImageGenerator.FILTERS_KEY.keys():
        return abort(404, description='Band key not found')
    
    if folder not in ['images', 'histograms']:
        return abort(404, description='Image type not found')

    image_path = getFilePath(session_id, f'{band_key}.png', folder)
    if not image_path:
        return abort(404, description='Image not found')
    
    return send_file(image_path, mimetype='image/png')
    

