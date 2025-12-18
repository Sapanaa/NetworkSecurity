from network_security.components.data_ingestion import DataIngestion
from network_security.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.components.data_validation import DataValidation


if __name__ == "__main__":
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion_and_split()
    print(f"Data Ingestion Artifact: {data_ingestion_artifact}")
    data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
    data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
    data_validation_artifact = data_validation.initiate_data_validation()