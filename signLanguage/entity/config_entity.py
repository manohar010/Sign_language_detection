import os
from dataclasses import dataclass
from datetime import datetime
from signLanguage.constant.training_pipeline import *

# Generating a timestamp to uniquely identify each training run
TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass
class TrainingPipelineConfig:
    # Root directory for all artifacts generated during this execution
    artifacts_dir: str = os.path.join(ARTIFACTS_DIR, TIMESTAMP)

# Global instance of the pipeline configuration
training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    # Directory for data ingestion artifacts
    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_INGESTION_DIR_NAME
    )

    # Path to store the downloaded feature data
    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR  # <--- Typo fixed here!
    )

    # Source URL for downloading the dataset
    data_download_url: str = DATA_DOWNLOAD_URL

@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_VALIDATION_DIR_NAME
    )

    valid_data_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_VALID_DIR)
    invalid_data_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_INVALID_DIR)