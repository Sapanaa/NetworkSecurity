from network_security.components.data_ingestion import DataIngestion
from network_security.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer
import sys

if __name__ == "__main__":
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion_and_split()
    print(f"Data Ingestion Artifact: {data_ingestion_artifact}")
    data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
    data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
    data_validation_artifact = data_validation.initiate_data_validation()

    print(f"Data Validation Artifact: {data_validation_artifact}")
    data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)
    data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact, data_transformation_config=data_transformation_config)
    data_transformation_artifact = data_transformation.initiate_data_transformation()
    print(f"Data Transformation Artifact: {data_transformation_artifact}")

    model_trainer_config = ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
    model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
    model_trainer_artifact = model_trainer.initiate_model_trainer()
    print(f"Model Trainer Artifact: {model_trainer_artifact}")
