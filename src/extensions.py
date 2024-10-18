""" LOGGER """
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)





""" SUPRIMIR WARNINGS DE DEPRECIACIÓN """

import warnings
from sklearn.exceptions import InconsistentVersionWarning

# Suprimir UserWarnings de xgboost
warnings.filterwarnings("ignore", category=UserWarning, module='xgboost.core')

# Suprimir InconsistentVersionWarning de scikit-learn
warnings.filterwarnings("ignore", category=InconsistentVersionWarning, module='sklearn.base')
