import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
from fastapi import FastAPI,Request, Response

logger = logging.getLogger('compute_logger')
logger.setLevel(logging.DEBUG)
log_directory = 'logs'

os.makedirs(log_directory, exist_ok=True)

current_date = datetime.now().strftime('%Y-%m-%d')
log_filename = f'{log_directory}/app_{current_date}.log'

handler = RotatingFileHandler(
    log_filename,
    maxBytes=5 * 1024 * 1024,  
    backupCount=0              
)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)