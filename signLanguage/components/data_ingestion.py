import os
import sys
from six.moves import urllib 
import zipfile
from signLanguage.logger import logging
from signLanguage.exception import signException
from signLanguage.entity.config_entity import DataIngestionConfig
from signLanguage.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise signException(e, sys)

    def download_data(self) -> str:
        """
        Fetch data from the url
        """
        try:
            dataset_url = self.data_ingestion_config.data_download_url
            zip_download_dir = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(zip_download_dir, exist_ok=True)
            data_file_name = os.path.basename(dataset_url)
            zip_file_path = os.path.join(zip_download_dir, data_file_name)
            
            logging.info(f"Downloading data from {dataset_url} into file {zip_file_path}")
            urllib.request.urlretrieve(dataset_url, zip_file_path)
            logging.info(f"Downloaded data from {dataset_url} into file {zip_file_path}")
            
            return zip_file_path
        
        except Exception as e:
            raise signException(e, sys)

    def extract_zip_file(self, zip_file_path: str) -> str:
        """
        Extracts the zip file into the feature store directory
        """
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(feature_store_path, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(feature_store_path)
            logging.info(f"Extracted zip file {zip_file_path} into directory {feature_store_path}")

            return feature_store_path
        
        except Exception as e:
            raise signException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of DataIngestion class")
        try:
            zip_file_path = self.download_data()
            feature_store_path = self.extract_zip_file(zip_file_path)

            data_store_path = os.path.join(feature_store_path, "Sign_language_data")

            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path=zip_file_path,
                feature_store_path=feature_store_path
            )
            
            logging.info("Exited initiate_data_ingestion method of DataIngestion class")
            logging.info(f"Data Ingestion artifact: {data_ingestion_artifact}")
            
            return data_ingestion_artifact
         
        except Exception as e:
            raise signException(e, sys)
        