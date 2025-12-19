import sys
import pandas as pd
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact, DataTransformationArtifact
from network_security.entity.config_entity import DataTransformationConfig
import numpy as np
import os
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from network_security.constant.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from network_security.utils.main_utils.utils import save_object, save_numpy_array_data




class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            if data_validation_artifact is None:
                raise NetworkSecurityException(
                    "DataValidationArtifact is None. Validation stage failed.",
                    sys
                )

            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            logging.info(f"Reading data from file: {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformer_object(self) -> Pipeline:
        try:
            logging.info("Creating data transformer object")
            return KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")

            # Create directories
            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_train_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_test_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_object_file_path), exist_ok=True)

            train_df = self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = self.read_data(self.data_validation_artifact.valid_test_file_path)

            X_train = train_df.drop(columns=[TARGET_COLUMN])
            y_train = train_df[TARGET_COLUMN].replace(-1, 0)

            X_test = test_df.drop(columns=[TARGET_COLUMN])
            y_test = test_df[TARGET_COLUMN].replace(-1, 0)

            preprocessor = self.get_data_transformer_object()
            preprocessor.fit(X_train)

            X_train_arr = preprocessor.transform(X_train)
            X_test_arr = preprocessor.transform(X_test)

            train_arr = np.c_[X_train_arr, y_train.to_numpy()]
            test_arr = np.c_[X_test_arr, y_test.to_numpy()]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
            )

            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            logging.info("Data transformation completed successfully")
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
