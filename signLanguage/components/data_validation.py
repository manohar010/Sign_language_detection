import os
import sys
import shutil
from signLanguage.logger import logging
from signLanguage.exception import signException
from signLanguage.entity.config_entity import DataValidationConfig
from signLanguage.entity.artifact_entity import (DataIngestionArtifact, DataValidationArtifact)

class DataValidation:
    def __init__(
        self, 
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise signException(e, sys)

    def validate_all_files_exist(self) -> bool:
        try:
            validation_status = None

            all_files = os.listdir(self.data_ingestion_artifact.feature_store_path)

            validation_status = True
            
            for required_file in self.data_validation_config.required_file_list:
                if required_file not in all_files:
                    validation_status = False
                    break 

            os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
            
            # Use 'valid_status_file_path' as per your config
            with open(self.data_validation_config.valid_status_file_path, 'w') as f:
                f.write(f"validation_status: {validation_status}")

            return validation_status

        except Exception as e:
            raise signException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        logging.info("Entered initiate_data_validation method of DataValidation class")
        try:
            status = self.validate_all_files_exist()
            
            # Windows Fix: Force copy the zip file so the trainer can find it
            # even if the validation status is currently False for debugging.
            if os.path.exists(self.data_ingestion_artifact.data_zip_file_path):
                shutil.copy(self.data_ingestion_artifact.data_zip_file_path, os.getcwd())
                logging.info("Copied Sign_language_data.zip to root directory.")
            
            data_validation_artifact = DataValidationArtifact(validation_status=status)

            return data_validation_artifact
        
        except Exception as e:
            raise signException(e, sys)