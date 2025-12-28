import os
import sys
import yaml
import zipfile
import shutil
from signLanguage.utils.main_utils import read_yaml_file
from signLanguage.logger import logging
from signLanguage.exception import signException
from signLanguage.entity.config_entity import ModelTrainerConfig
from signLanguage.entity.artifact_entity import ModelTrainerArtifact

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig):
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method")
        try:
            # 1. Windows Compatible Extraction
            if not os.path.exists("Sign_language_data.zip"):
                raise FileNotFoundError("Sign_language_data.zip not found in root directory!")

            logging.info("Extracting data...")
            with zipfile.ZipFile("Sign_language_data.zip", 'r') as zip_ref:
                zip_ref.extractall(".")
            
            # Fix nested folder issue (Common on Windows)
            if not os.path.exists("data.yaml"):
                folders = [f for f in os.listdir('.') if os.path.isdir(f) and f not in ['yolov5', 'signLanguage', 'artifacts']]
                for folder in folders:
                    if os.path.exists(os.path.join(folder, "data.yaml")):
                        logging.info(f"Moving files from {folder} to root")
                        for item in os.listdir(folder):
                            shutil.move(os.path.join(folder, item), ".")
                        break

            # 2. Configure YOLOv5 nc
            with open("data.yaml", 'r') as stream:
                num_classes = str(yaml.safe_load(stream)['nc'])

            model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]
            config = read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")
            config['nc'] = int(num_classes)
            
            with open(f'yolov5/models/custom_{model_config_file_name}.yaml', 'w') as f:
                yaml.dump(config, f)

            # 3. Training Command for Windows
            os.system(f"cd yolov5 && python train.py --img 416 --batch {self.model_trainer_config.batch_size} "
                      f"--epochs {self.model_trainer_config.no_epochs} --data ../data.yaml "
                      f"--cfg ./models/custom_{model_config_file_name}.yaml --weights {self.model_trainer_config.weight_name} "
                      f"--name yolov5s_results --cache")

            # 4. Save Artifacts
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            shutil.copy("yolov5/runs/train/yolov5s_results/weights/best.pt", 
                        os.path.join(self.model_trainer_config.model_trainer_dir, "best.pt"))

            return ModelTrainerArtifact(
                trained_model_file_path=os.path.join(self.model_trainer_config.model_trainer_dir, "best.pt")
            )

        except Exception as e:
            raise signException(e, sys)