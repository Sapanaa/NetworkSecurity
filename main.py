from network_security.components.data_ingestion import DataIngestion
from network_security.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig



if __name__ == "__main__":
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion_and_split()
    print(f"Data Ingestion Artifact: {data_ingestion_artifact}")