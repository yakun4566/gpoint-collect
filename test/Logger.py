#-*- coding:utf-8 -*-
import logging
import logging.config
import os
import yaml


def setup_logging(default_path="resources/logging.yml", name=None, default_level=logging.INFO, env_key="LOG_CFG"):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    return logging.getLogger(name)