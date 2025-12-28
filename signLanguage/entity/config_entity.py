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
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORN_DIR
    )

    # Source URL for downloading the dataset
    data_download_url: str = DATA_DOWNLOAD_URL

@dataclass
class DataValidationConfig:
    # Directory for data validation artifacts
    data_validation_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_VALIDATION_DIR_NAME
    )

    # Path to the file containing validation status (True/False)
    valid_status_file_path: str = os.path.join(
        data_validation_dir, DATA_VALIDATION_STATUS_FILE
    )
    
    # List of files required for the project to proceed
    required_file_list = DATA_VALIDATION_ALL_REQUIRED_FILE_LIST

@dataclass
class ModelTrainerConfig:
    # Directory where the trained YOLOv5 model weights will be saved
    model_trainer_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_TRAINING_ARTIFACTS_DIR
    )

    # Pre-trained YOLOv5 weight file name (e.g., yolov5s.pt)
    weight_name: str = MODEL_TRAINER_PRETRAINED_WEIGHT_NAME

    # Training parameters for your 324 images
    no_epochs: int = MODEL_TRAINER_NO_EPOCHS
    batch_size: int = MODEL_TRAINER_BATCH_SIZE