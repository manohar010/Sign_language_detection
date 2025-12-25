from signLanguage.logger import logging
from signLanguage.exception import signException
import sys
from signLanguage.pipeline.train_pipeline import TrainPipeline



if __name__ == "__main__":
    obj = TrainPipeline()
    obj.run_pipeline()
    print("Pipeline executed successfully")