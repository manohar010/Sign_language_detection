import os

ARTIFACTS_DIR: str = "artifacts"

# --- Data Ingestion Constants ---
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"

# Use the standard shareable link with gdown
DATA_DOWNLOAD_URL: str = "https://drive.google.com/file/d/1LKZGUkk_Wj75m_BL89zhMqHHWU-BgbHZ/view?usp=sharing"

# --- Data Validation Constants ---
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_STATUS_FILE: str = "status.txt"
DATA_VALIDATION_ALL_REQUIRED_FILES: list = ["train", "test", "data.yaml"]