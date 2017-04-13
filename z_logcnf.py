# _*_ coding: utf-8 _*_

import logging


def log_init(logging_name):
    file_log_info = "./dou.log"
    logger_info = logging.getLogger(name=logging_name)

    handler_info = logging.FileHandler(filename=file_log_info, encoding="utf-8")
    datefmt = '%Y-%m-%d %H:%M:%S'
    format_str = '%(asctime)s\t%(levelname)s\t%(message)s '
    formatter = logging.Formatter(format_str, datefmt)
    handler_info.setFormatter(formatter)

    logger_info.addHandler(handler_info)
    logger_info.setLevel(logging.DEBUG)

    return logger_info


if __name__ == "__main__":
    logger = log_init("test")
    print(logger.name)
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
