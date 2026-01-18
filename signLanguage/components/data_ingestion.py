import os
import sys
import gdown
import zipfile
from signLanguage.logger import logging
from signLanguage.exception import SignException
from signLanguage.entity.config_entity import DataIngestionConfig
from signLanguage.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SignException(e, sys)

    def download_data(self) -> str:
        '''
        Fetch data from google drive using gdown (handles large files)
        '''
        try:
            dataset_url = self.data_ingestion_config.data_download_url
            zip_download_dir = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(zip_download_dir, exist_ok=True)
            data_file_name = "Sign_language_data.zip"
            zip_file_path = os.path.join(zip_download_dir, data_file_name)
            
            logging.info(f"Downloading file from :{dataset_url} into :{zip_file_path}")
            
            # Using gdown for large Drive files
            gdown.download(dataset_url, zip_file_path, quiet=False, fuzzy=True)
            
            logging.info(f"downloaded file from :{dataset_url} into :{zip_file_path}")
            
            return zip_file_path
        
        except Exception as e:
            raise SignException(e, sys)
        
    def extracct_zip_file(self, zip_file_path: str)-> str:
        '''
        zip_file_path: str
        extracts the zip file into the data ingestion directory
        function returns none
        '''
        try:
            # --- FIX IS HERE ---
            # We changed .feature_store_dir to .feature_store_file_path to match your config
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            
            os.makedirs(feature_store_path, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(feature_store_path)
            logging.info(f"extracted zip file : {zip_file_path} into dir : {feature_store_path}")
        
            return feature_store_path
        
        except Exception as e:
            raise SignException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered the data ingestion method")
        try:
            zip_file_path = self.download_data()
            feature_store_path = self.extracct_zip_file(zip_file_path)

            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path=zip_file_path,
                feature_store_path=feature_store_path
            )
             
            logging.info(f"exited initiate_data_ingestion method of Data ingestion class")
            logging.info(f"Data Ingestion artifact : {data_ingestion_artifact}")

            return data_ingestion_artifact
             
        except Exception as e:
            raise SignException(e, sys)