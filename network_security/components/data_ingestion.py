from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.entity.artifact_entity import DataIngestionArtifact
import sys
import os
from sklearn.model_selection import train_test_split
import pymongo
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        feature_store_file_path = None  # defensive
        try:
            logging.info("Starting data ingestion from Mongodb")

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # ensure directory exists
            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)

            cursor = pymongo.MongoClient(MONGO_DB_URL)[
                self.data_ingestion_config.database_name
            ][
                self.data_ingestion_config.collection_name
            ].find()

            df = pd.DataFrame(list(cursor))

            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            df.replace(to_replace=["?", "NA"], value=pd.NA, inplace=True)

            logging.info(f"Saving data in feature store: {feature_store_file_path}")
            df.to_csv(feature_store_file_path, index=False)

            logging.info("Data ingestion completed successfully")

        except Exception as e:
            logging.error(
                f"Data ingestion failed. feature_store_file_path={feature_store_file_path}"
            )
            raise NetworkSecurityException(e, sys)


            
        
    def split_data_as_train_test(self):

        training_file_path = None
        testing_file_path = None

        try:
            logging.info("Starting data split into train and test set")

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            training_file_path = self.data_ingestion_config.training_file_path
            testing_file_path = self.data_ingestion_config.testing_file_path

            df = pd.read_csv(feature_store_file_path)

            train_set, test_set = train_test_split(
                df,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )

            os.makedirs(os.path.dirname(training_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(testing_file_path), exist_ok=True)

            logging.info(f"Saving train data to {training_file_path}")
            train_set.to_csv(training_file_path, index=False, header=True)

            logging.info(f"Saving test data to {testing_file_path}")
            test_set.to_csv(testing_file_path, index=False, header=True)

            logging.info("Data split completed successfully")

        except Exception as e:
            logging.error(
                f"Train-test split failed. "
                f"training_file_path={training_file_path}, "
                f"testing_file_path={testing_file_path}"
            )
            raise NetworkSecurityException(e, sys)

        
    
    def initiate_data_ingestion_and_split(self):
        '''Method to initiate data ingestion and split'''
        try:
            self.initiate_data_ingestion()
            self.split_data_as_train_test()
            dataartifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return dataartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
