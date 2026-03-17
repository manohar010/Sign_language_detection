import os
import sys
import yaml
import shutil
import zipfile
from signLanguage.logger import logging
from signLanguage.exception import SignException
from signLanguage.entity.config_entity import ModelTrainerConfig
from signLanguage.entity.artifact_entity import ModelTrainerArtifact
from ultralytics import YOLO

class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            # ---------------------------------------------------------
            # 1. Unzip the Data
            # ---------------------------------------------------------
            logging.info("Unzipping data...")
            if os.path.exists("Sign_language_data.zip"):
                with zipfile.ZipFile("Sign_language_data.zip", 'r') as zip_ref:
                    zip_ref.extractall(".")
                os.remove("Sign_language_data.zip")

            # ---------------------------------------------------------
            # 2. Fix Data Structure (Find 'train' folder)
            # ---------------------------------------------------------
            if not os.path.exists("train"):
                print("Root 'train' folder not found. Searching subfolders...")
                for root, dirs, files in os.walk("."):
                    if "train" in dirs:
                        hidden_path = os.path.join(root, "train")
                        parent_folder = os.path.dirname(hidden_path)
                        print(f"Found data inside: {parent_folder}")
                        
                        for item in os.listdir(parent_folder):
                            src = os.path.join(parent_folder, item)
                            dst = os.path.join(".", item)
                            if not os.path.exists(dst):
                                shutil.move(src, dst)
                        break
            
            # ---------------------------------------------------------
            # 3. Create data.yaml (Updated for 9 classes)
            # ---------------------------------------------------------
            print("\n" + "!"*50)
            print("!!! GENERATING NEW DATA.YAML FOR YOLO11 !!!")
            
            val_folder = "test"
            if not os.path.exists("test") and os.path.exists("val"):
                val_folder = "val"
            
            cwd = os.getcwd()
            data_content = {
                'train': os.path.join(cwd, "train", "images"),
                'val': os.path.join(cwd, val_folder, "images"),
                'test': os.path.join(cwd, val_folder, "images"),
                'nc': 9,
                'names': ['Hello', 'Help', 'ILoveYou', 'No', 'Please', 'Sorry', 'Thanks', 'Water', 'Yes']
            }
            
            with open("data.yaml", 'w') as f:
                yaml.dump(data_content, f)
                
            print(f"data.yaml created with 9 classes.")
            print("!"*50 + "\n")

            # ---------------------------------------------------------
            # 4. Train with YOLO11
            # ---------------------------------------------------------
            epochs = self.model_trainer_config.no_epochs
            batch_size = self.model_trainer_config.batch_size
            
            # !!! BULLETPROOF FIX !!! 
            # Hardcoded to bypass any configuration file errors
            model_name = "yolo11s.pt" 
            
            logging.info(f"Loading YOLO model: {model_name}")
            model = YOLO(model_name)

            logging.info(f"Starting training for {epochs} epochs...")
            
            model.train(
                data="data.yaml",
                epochs=epochs,
                batch=batch_size,
                imgsz=416,
                name="yolo11_results",  # Changed folder name
                exist_ok=True,          
                device="cpu",           
                workers=0               
            )

            # ---------------------------------------------------------
            # 5. Save Artifacts
            # ---------------------------------------------------------
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            
            # Update paths to look in the new yolo11_results folder
            source_best = "runs/detect/yolo11_results/weights/best.pt"
            dest_best = os.path.join(self.model_trainer_config.model_trainer_dir, "best.pt")

            if os.path.exists(source_best):
                shutil.copy(source_best, dest_best)
                logging.info(f"Model saved to {dest_best}")
            else:
                alt_source = "runs/train/yolo11_results/weights/best.pt"
                if os.path.exists(alt_source):
                    shutil.copy(alt_source, dest_best)
                    logging.info(f"Model saved to {dest_best} (from fallback path)")
                else:
                    logging.warning(f"Training finished but best.pt not found at {source_best}")

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=dest_best
            )
            
            return model_trainer_artifact

        except Exception as e:
            raise SignException(e, sys)