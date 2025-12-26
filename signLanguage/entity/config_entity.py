import os
from dataclasses import dataclass
from datetime import datetime
from signLanguage.constant.training_pipeline import *

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%S")

@dataclass
class TrainingpipelineConfig:
    artifacts_dir: str = os.path.join(ARTIFACTS_DIR,TIMESTAMP)



training_pipline_config:TrainingpipelineConfig = TrainingpipelineConfig()


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(
        training_pipline_config.artifacts_dir, DATA_INGESTION_DIR_NAME  
    )

    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORN_DIR
    )

    data_download_url:str = DATA_DOWNLOAD_URL



@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(
        training_pipline_config.artifacts_dir, DATA_VALIDATION_DIR_NAME
    )

    valid_status_file_path: str = os.path.join(
        data_validation_dir, DATA_VALIDATION_STATUS_FILE
    )
   
    required_file_list = DATA_VALIDATION_ALL_REQUIRED_FILE_LIST