from datetime import datetime
import os

from network_security.constant import training_pipeline as tp

print(f"Target Column: {tp.TARGET_COLUMN}")
print(f"Pipeline Name: {tp.PIPELINE_NAME}")


class TrainingPipelineConfig:
    def __init__(self, timestamp = datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        
        self.pipeline_name = tp.PIPELINE_NAME
        self.artifact_dir = tp.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_dir, timestamp)
        self.timestamp: str= timestamp

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: tp.TrainingPipelineConfig):
        self.pipeline_name = training_pipeline_config.pipeline_name
        self.artifact_dir = training_pipeline_config.artifact_dir
        self.data_ingestion_dir = tp.DATA_INGESTION_DIR_NAME
        self.feature_store_dir = tp.DATA_INGESTION_FEATURE_STORE_DIR
        self.ingested_dir = tp.DATA_INGESTION_INGESTED_DIR
        self.train_file_name = tp.TRAIN_FILE_NAME
        self.test_file_name = tp.TEST_FILE_NAME
        self.train_test_split_ratio = tp.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.database_name = tp.DATA_INGESTION_DATABASE_NAME
        self.collection_name = tp.DATA_INGESTION_COLLECTION_NAME

    def get_data_ingestion_artifact_dir(self) -> str:
        timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        return os.path.join(
            self.artifact_dir,
            self.data_ingestion_dir,
            timestamp
        )