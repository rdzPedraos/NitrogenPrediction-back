from flask import Blueprint

main_blueprint = Blueprint('main', __name__)

# Importar las rutas individuales
from .status_route import up
from .upload_route import upload_images
from .process_route import process
from .get_status_route import get_status
#from .get_image_route import get_processed_image
#from .predict_route import predict
