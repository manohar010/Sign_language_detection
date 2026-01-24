import os

ARTIFACTS_DIR: str = "artifacts"

# --- Data Ingestion Constants ---
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"

# Use the standard shareable link with gdown
DATA_DOWNLOAD_URL: str = "https://github.com/manohar010/Sing_data/raw/refs/heads/main/Sign_language_data.zip"

# --- Data Validation Constants ---
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_STATUS_FILE: str = "status.txt"
DATA_VALIDATION_ALL_REQUIRED_FILES: list = ["train", "test", "data.yaml"]


# --- Model Trainer Constants ---
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_PRETRAINED_WEIGHT_NAME: str = "yolov5s.pt"
MODEL_TRAINER_NO_EPOCHS: int = 100 
MODEL_TRAINER_BATCH_SIZE: int = 16