# -*- coding:utf-8 -*-
from loguru import logger
loggers = {}

PATH = 'logs/gpoint-collect.log'
LEVEL = "INFO"
ROTATION = "20 MB"
RETENTION='30 DAYS'
logger.add(PATH, level=LEVEL, rotation=ROTATION, retention=RETENTION, encoding="utf-8")
def get_logger():
    global loggers
    return logger
    pass
