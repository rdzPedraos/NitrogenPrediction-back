from utils.index_calculations import calculate_indices, generate_rgb_image
import micasense.capture as capture
import micasense.imageutils as imageutils
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import base64

from utils.session_manager import load_session_data, save_session_data, update_session_status
from config import Config

def process_images(session_id):
    session_data = load_session_data(session_id)
    if not session_data:
        print(f"Session {session_id} not found.")
        return

    storage_path = session_data['storage_path']

    # Encontrar archivos de imágenes
    image_files = glob.glob(os.path.join(storage_path, '*.tif'))

    try:
        if len(image_files) == 0:
            update_session_status(session_id, 'error')
            return

        cap = capture.Capture.from_filelist(image_files)

        # Alinear imágenes
        warp_matrices, _ = imageutils.align_capture(cap)
        im_aligned = imageutils.aligned_capture(cap, warp_matrices)

        # Guardar im_aligned para uso posterior
        im_aligned_path = os.path.join(storage_path, 'im_aligned.npy')
        np.save(im_aligned_path, im_aligned)
        session_data['im_aligned_path'] = im_aligned_path

        # Generar imagen RGB
        rgb_image = generate_rgb_image(im_aligned, cap)
        rgb_image_path = os.path.join(storage_path, 'rgb.png')
        plt.imsave(rgb_image_path, rgb_image)
        session_data['images']['rgb'] = rgb_image_path
        save_session_data(session_id, session_data)
        emit_image(session_id, 'rgb', rgb_image_path)

        # Calcular índices de vegetación
        indices = calculate_indices(im_aligned, cap)
        for index_name, index_data in indices.items():
            index_image_path = os.path.join(storage_path, f'{index_name}.png')
            plt.imsave(index_image_path, index_data, cmap='RdYlGn')
            session_data['images'][index_name] = index_image_path

            # Guardar índice para uso posterior
            index_data_path = os.path.join(storage_path, f'{index_name}.npy')
            np.save(index_data_path, index_data)
            session_data[index_name] = index_data_path

            save_session_data(session_id, session_data)
            emit_image(session_id, index_name, index_image_path)

        # Actualizar el estado de la sesión
        session_data['status'] = 'processed'
        save_session_data(session_id, session_data)

    except Exception as e:
        update_session_status(session_id, 'error')
        print(f"Error processing images for session {session_id}: {e}")

def emit_image(session_id, image_type, image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
