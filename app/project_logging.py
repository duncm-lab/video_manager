"""shared logging object"""
import os
import logging


from app.config import LogConfig as cfg


if not os.path.exists(cfg.log_location):
    log_path = './'
else:
    log_path = cfg.log_location


logging.basicConfig(filename=os.path.join(log_path, 'app.log'),
                    level=cfg.log_level,
                    format='%(asctime)s %(levelname)s %(module)s'
                    '%(lineno)s %(funcName)s %(message)s')
logger = logging.getLogger()
