import os

ARTIFACTS_DIR: str = "artifacts"


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_DIR_NAME: str = "data_ingestion"

DATA_INGESTION_FEATURE_STORN_DIR: str = "feature_store"

DATA_DOWNLOAD_URL: str = "https://github.com/manohar010/Sing_data/raw/refs/heads/main/Sign_language_data.zip"





"""
Data Validation related constant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"

DATA_VALIDATION_STATUS_FILE = 'status.txt'

DATA_VALIDATION_ALL_REQUIRED_FILE_LIST = ["train", "test", "data.yaml"]


# Model Trainer related constants
DATA_TRAINING_KEY = "yolov5"
DATA_TRAINING_ARTIFACTS_DIR = "model_trainer"

MODEL_TRAINER_PRETRAINED_WEIGHT_NAME = "yolov5s.pt" 
MODEL_TRAINER_NO_EPOCHS = 100  # Increase for better accuracy
MODEL_TRAINER_BATCH_SIZE = 16