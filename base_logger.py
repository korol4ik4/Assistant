import logging
import sys
import os


def get_base_logger(log_file_name, logger_name, log_level):
    path = "log"
    if not os.path.exists(path):
        os.mkdir(path)
    log_file_name = path + os.sep + log_file_name
    print(logger_name)
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    fh = logging.FileHandler(log_file_name, mode = "w")
    sh = logging.StreamHandler(stream=sys.stdout)
    fform = logging.Formatter(fmt='[%(asctime)s] : %(levelname)s %(name)s %(message)s')
    sform = logging.Formatter(fmt='%(levelname)s %(name)s %(message)s')
    fh.setFormatter(fform)
    sh.setFormatter(sform)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger