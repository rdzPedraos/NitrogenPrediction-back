from flask import jsonify
from . import main_blueprint

from utils.FileManager import getBandFiles
from utils.ImageProcessor import ImageProcessor
from utils.ImageGenerator import ImageGenerator

@main_blueprint.route('/<session_id>/process', methods=['POST'])
def process(session_id):
    bands = getBandFiles(session_id, "bands")
    panels = getBandFiles(session_id, "panels")

    # Crear una instancia de ImageProcessor
    processor = ImageProcessor(bands, panels)

    # Crear una instancia de ImageGenerator
    generator = ImageGenerator(processor, session_id)
    
    # Generar y guardar la imagen RGB
    generator.generate_rgb()
    generator.save_rgb_image()

    # Calcular los índices de vegetación
    generator.compute_indices()

    # Aplicar máscara a los índices
    generator.mask_indices()

    # Generar y guardar las salidas de los índices
    generator.generate_and_save_index_outputs()
    
    generator.save_indices()

    return jsonify({'message': 'Processing completed', 'session_id': session_id}), 200
