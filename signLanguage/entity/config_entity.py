import os
from dataclasses import dataclass, field  # <--- Added 'field' to imports
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
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR
    )

    # Source URL for downloading the dataset
    data_download_url: str = DATA_DOWNLOAD_URL

@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_VALIDATION_DIR_NAME
    )

    valid_status_file_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_STATUS_FILE)

    # --- FIX BELOW ---
    # We use field(default_factory=...) to correctly handle the list assignment
    required_file_list: list = field(default_factory=lambda: DATA_VALIDATION_ALL_REQUIRED_FILES)