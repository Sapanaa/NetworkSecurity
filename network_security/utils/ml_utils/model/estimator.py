from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
import sys
import os
from network_security.utils.main_utils.utils import save_object, load_object, save_numpy_array_data, load_numpy_array_data
from network_security.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def predict(self, X):
        try:
            X_transformed = self.preprocessor.transform(X)
            predictions = self.model.predict(X_transformed)
            return predictions
        except Exception as e:
            raise NetworkSecurityException(e,sys)

