import os
import logging
from datetime import datetime

LOG_DIR = '.printbot'
LOG_FILE = os.path.join(LOG_DIR, 'print_log.csv')
BOT_LOG = os.path.join(LOG_DIR, 'bot.log')

# Создаём папку, если её нет
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(BOT_LOG),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def log_print_status(filename, status, user_id):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()},{filename},{status},{user_id}\n")
