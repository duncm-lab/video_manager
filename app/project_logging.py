"""shared logging object"""
import os
import logging


import app.config as cfg # pylint: disable=wrong-import-position


if not os.path.exists(cfg.QUEUE_PROCESSOR_LOG):
    log_path = './'
else:
    log_path = cfg.QUEUE_PROCESSOR_LOG


logging.basicConfig(filename=os.path.join(log_path, 'app.log'),
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(module)s'
            '%(lineno)s %(funcName)s %(message)s')
logger = logging.getLogger()
