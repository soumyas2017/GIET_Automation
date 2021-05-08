from automation.admission import Admission
from utilties.config import breaker_file, log_file_path
import os
import logging
import logging.config
logging.FileHandler(log_file_path, mode='a', encoding=None, delay=False,)
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('main')

def do_activity():
    logger.info('Start Activity')
    ob = Admission()
    ob.Main()


while True:
    if not os.path.exists(breaker_file):
        do_activity()
    else:
        logger.info("Break file detected.. Quitting..")
        break