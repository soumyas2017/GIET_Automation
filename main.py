from automation.new_application import Application
from utilties.helpers import *
from utilties.config import get_env
import os
import schedule
import time
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('main')


def do_activity(vars):
    ob = Application()
    with get_temporary_cache() as cached:
        ob.Main(
            login_url=vars['login_url'],
            registration_url=vars["registration_url"],
            win_cred_file=vars["win_cred_file"],
            mock_data_file=vars["mock_data_file"],
            chrome_driver_path=vars["chrome_driver_path"],
            firefox_driver_path=vars["firefox_driver_path"],
            breaker_file=vars["breaker_file"],
            apply_success=vars["apply_success"],
            apply_failure=vars["apply_failure"],
            cached=cached
        )
        logger.info('Start Activity')


if __name__ == '__main__':
    vars = get_env()
    while True:
        if not os.path.exists(vars["breaker_file"]):
            try:
                do_activity(vars)
            except Exception as e:
                logger.exception("Exception.. Sleeping for 20 secs")
                time.sleep(20)
        else:
            logger.info("Break file detected.. Quitting..")
            break