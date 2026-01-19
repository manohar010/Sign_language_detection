from signLanguage.logger import logging
from signLanguage.exception import SignException
import sys
from signLanguage.pipeline.train_pipeline import TrainPipeline



if __name__ == "__main__":
    object = TrainPipeline()
    object.run_pipeline()
    print("Pipeline executed successfully")