from flask import request, send_file, abort
import io

from . import main_blueprint
from utils.ImageGenerator import ImageGenerator
from utils.FileManager import getFilePath, getCoordinatesFromPercentage, cutImage

@main_blueprint.route('/<session_id>/storage/<folder>/<band_key>', methods=['GET'])
def get_processed_image(session_id, folder, band_key):
    if band_key not in ImageGenerator.FILTERS_KEY.keys() and band_key != "rgb":
        return abort(404, description='Band key not found')
    
    if folder not in ['images', 'histograms']:
        return abort(404, description='Image type not found')

    image_path = getFilePath(session_id, f'{band_key}.png', folder)
    if not image_path:
        return abort(404, description='Image not found')
    
    coords = request.args.to_dict()
    if "crop" in coords:
        if not all(key in coords for key in ['x', 'y', 'width', 'height']):
            return abort(400, description='Missing coordinates')

        coords = getCoordinatesFromPercentage(image_path, coords) # Convertir las coordenadas a píxeles
        cropped_img = cutImage(image_path, coords)

        # Guardar la imagen recortada en memoria
        img_io = io.BytesIO()
        cropped_img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')
    
    return send_file(image_path, mimetype='image/png')
    

