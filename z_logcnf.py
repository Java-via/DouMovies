# _*_ coding: utf-8 _*_

import logging


def log_init():
    file_log_info = "info.log"
    logger_info = logging.getLogger(name="fetch_log")

    handler_info = logging.FileHandler(file_log_info)
    datefmt = '%Y-%m-%d %H:%M:%S'
    format_str = '%(asctime)s\t%(levelname)s\t%(message)s '
    formatter = logging.Formatter(format_str, datefmt)
    handler_info.setFormatter(formatter)

    logger_info.addHandler(handler_info)
    logger_info.setLevel(logging.INFO)

    return logger_info
