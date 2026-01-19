import os
import sys
import yaml
import shutil
import zipfile
from signLanguage.logger import logging
from signLanguage.exception import SignException
from signLanguage.entity.config_entity import ModelTrainerConfig
from signLanguage.entity.artifact_entity import ModelTrainerArtifact

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
            # 1.5. FIX: Find and Move 'train' folder (The fix for "Dataset not found")
            # ---------------------------------------------------------
            # If 'train' is not in the root, find where it is hiding
            if not os.path.exists("train"):
                print("Root 'train' folder not found. Searching subfolders...")
                for root, dirs, files in os.walk("."):
                    if "train" in dirs:
                        # Found the subfolder containing train
                        hidden_path = os.path.join(root, "train")
                        parent_folder = os.path.dirname(hidden_path)
                        
                        print(f"Found data inside: {parent_folder}")
                        
                        # Move contents of that folder to the root
                        for item in os.listdir(parent_folder):
                            src = os.path.join(parent_folder, item)
                            dst = os.path.join(".", item)
                            if not os.path.exists(dst):
                                shutil.move(src, dst)
                        
                        # Cleanup empty folder
                        # shutil.rmtree(parent_folder)  # Optional
                        break
            
            # ---------------------------------------------------------
            # 2. Prepare YOLOv5
            # ---------------------------------------------------------
            if not os.path.exists("yolov5"):
                os.system(f"git clone https://github.com/ultralytics/yolov5") 

            # ---------------------------------------------------------
            # 3. FORCE CREATE data.yaml
            # ---------------------------------------------------------
            print("\n" + "!"*50)
            print("!!! GENERATING NEW DATA.YAML WITH nc=6 !!!")
            
            # Check if 'test' exists, if not, look for 'val'
            val_folder = "test"
            if not os.path.exists("test") and os.path.exists("val"):
                val_folder = "val"
                print("Found 'val' folder instead of 'test'. Using 'val'.")
            
            data_content = {
                'train': os.path.abspath(os.path.join(os.getcwd(), "train", "images")),
                'val': os.path.abspath(os.path.join(os.getcwd(), val_folder, "images")),
                'test': os.path.abspath(os.path.join(os.getcwd(), val_folder, "images")),
                'nc': 6,
                'names': ['Hello', 'yes', 'No', 'Thanks', 'Iloveyou', 'please']
            }
            
            with open("data.yaml", 'w') as f:
                yaml.dump(data_content, f)
            
            print(f"File created successfully.")
            print(f"Train Path: {data_content['train']}")
            print(f"Val Path:   {data_content['val']}")
            print("!"*50 + "\n")

            # ---------------------------------------------------------
            # 4. Prepare Model Config
            # ---------------------------------------------------------
            raw_weight_name = self.model_trainer_config.weight_name
            model_basename = raw_weight_name.replace(".pt", "") 
            
            config = yaml.safe_load(open(f"yolov5/models/{model_basename}.yaml"))
            config['nc'] = 6 
            
            with open(f'yolov5/models/custom_{model_basename}.yaml', 'w') as f:
                yaml.dump(config, f)

            # ---------------------------------------------------------
            # 5. Run Training
            # ---------------------------------------------------------
            batch_size = self.model_trainer_config.batch_size
            epochs = self.model_trainer_config.no_epochs
            
            logging.info(f"Starting training with {epochs} epochs...")
            
            os.system(f"cd yolov5 && python train.py --img 416 --batch {batch_size} --epochs {epochs} --data ../data.yaml --cfg ./models/custom_{model_basename}.yaml --weights {model_basename}.pt --name yolov5s_results --cache --workers 0")

            # ---------------------------------------------------------
            # 6. Save Artifacts
            # ---------------------------------------------------------
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            source_best = "yolov5/runs/train/yolov5s_results/weights/best.pt"
            dest_best = os.path.join(self.model_trainer_config.model_trainer_dir, "best.pt")

            if os.path.exists(source_best):
                shutil.copy(source_best, dest_best)
            else:
                logging.warning("Training finished but best.pt not found.")

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=dest_best
            )
            
            return model_trainer_artifact

        except Exception as e:
            raise SignException(e, sys)