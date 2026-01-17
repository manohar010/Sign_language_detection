import os.path
import sys
import yaml
import base64

from signLanguage.exception import SignException
from signLanguage.logger import logging



def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            logging.info("read ymal file successfuly")
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise SignException(e, sys) from e   
    


    def write_yaml_file(file_path: str, content: object, replace: bool =False) -> None:
        try:
    
            if replace:
                if os.path.exists(file_path):
                    os.remove(file_path)

            os.makedirs(os.path.dirname(file_path), exist_ok= True)

            with open(file_path, "w") as file:
                yaml.dump(content, file)
                logging.info("successfuly write_yaml_file")

        except Exception as e:
            raise SignException(e, sys) 
        

def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open("./data/" + fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def enocodeImageIntobase64(croppedImagepath):
    with open(croppedImagepath, "rb") as f:
        return base64.b64encode(f.read())
