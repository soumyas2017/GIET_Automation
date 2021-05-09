from automation.admission import Admission
from utilties.config import breaker_file, log_file_path
import os
import schedule
import time
import logging
import logging.config
logging.FileHandler(log_file_path, mode='a', encoding=None, delay=False,)
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('main')


def do_activity():
    logger.info('Start Activity')
    ob = Admission()
    ob.Main()


if __name__ == '__main__':
    while True:
        if not os.path.exists(breaker_file):
            try:
                do_activity()
            except Exception as e:
                logger.exception("Exception.. Sleeping for 20 secs")
                time.sleep(20)
        else:
            logger.info("Break file detected.. Quitting..")
            break