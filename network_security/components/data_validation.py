from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig

from network_security.exception.exception import NetworkSecurityException
from network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
import sys
import os

from sklearn.model_selection import train_test_split
import pandas as pd
from scipy.stats import ks_2samp


from network_security.constant.training_pipeline import SCHEMA_FILE_PATH
from network_security.utils.main_utils.utils import read_yaml_file

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataIngestionConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame)-> bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"required number of columns = {number_of_columns}")
            logging.info(f"Dataframe has {len(dataframe.columns)} columns")
            if len(dataframe.columns) == number_of_columns:
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def is_numerical_column_exist(self, dataframe:pd.DataFrame)->bool:
        try:
            status=True
            logging.info("Checking if all numerical columns are present")
            numerical_columns=self._schema_config["numerical_columns"]
            for column in numerical_columns:
                if column not in dataframe.columns:
                    status=False
            logging.info(f"All numerical columns are present: {status}")
            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_data_drift(self, base_dataframe:pd.DataFrame, current_dataframe:pd.DataFrame, threshold=0.05)->bool:
        try:
            status=True
            logging.info("Checking for data drift")
            numerical_columns=self._schema_config["numerical_columns"]
            drift_report={}
            for column in numerical_columns:
                base_data=base_dataframe[column]
                current_data=current_dataframe[column]
                p_value=ks_2samp(base_data, current_data).pvalue
                if p_value<threshold:
                    status=False
                drift_report[column]={
                    "p_value":float(p_value),
                    "drift_status":status
                }
            drift_report_file_path=self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            pd.DataFrame(drift_report).to_csv(drift_report_file_path)
            logging.info(f"Data drift detection completed: {status}")
            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_validation(self):
        try:
            logging.info("Starting data validation")
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            status=self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                raise Exception("Train data does not contain all columns")
            status=self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                raise Exception("Test data does not contain all columns")
            status=self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                raise Exception("Train data does not contain all numerical columns")
            status=self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                raise Exception("Test data does not contain all numerical columns")
            status=self.detect_data_drift(base_dataframe=train_dataframe, current_dataframe=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_data_dir)
            os.makedirs(dir_path, exist_ok=True)

            if not status:
                raise Exception("Data drift detected between train and test data")
            os.makedirs(self.data_validation_config.valid_data_dir, exist_ok=True)
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            logging.info("Data validation completed successfully")

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)