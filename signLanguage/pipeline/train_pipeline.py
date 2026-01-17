import sys, os
from signLanguage.logger import logging
from signLanguage.exception import SignException
from signLanguage.components.data_ingestion import DataIngestion
from signLanguage.entity.config_entity import DataIngestionConfig
from signLanguage.entity.artifact_entity import DataIngestionArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from the URL")

            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            
            # --- FIX IS HERE ---
            # You must call the method to get the artifact!
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            
            logging.info("Got the data_ingestion_artifact")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")

            return data_ingestion_artifact
        
        except Exception as e:
            raise SignException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            
        except Exception as e:
            raise SignException(e, sys)