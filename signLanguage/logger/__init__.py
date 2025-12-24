import logging
import os
from datetime import datetime
from from_root import from_root

# 1. Create the log file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# 2. Define the folder where logs will be stored (Fixed line 8)
log_path = os.path.join(from_root(), 'log')

# 3. Create the 'log' directory if it doesn't exist
os.makedirs(log_path, exist_ok=True)

# 4. Define the full path to the specific log file
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

# 5. Configure the logger
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)