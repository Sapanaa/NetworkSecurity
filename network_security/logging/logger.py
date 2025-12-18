import logging
import os
from datetime import datetime

LOG_DIR = "network_security/logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = f"{LOG_DIR}/network_security_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)