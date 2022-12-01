import logging
import configparser
from sys import platform
from xipraylib.files_holder import read_config, set_os_paths

_log_format = "[%(asctime)s] %(levelname)s [%(filename)s %(name)s %(funcName)s (%(lineno)d)]: %(message)s"
_log_format_journal = '[%(filename)s] %(message)s'

def get_file_handler(path = "/var/log/xipray.log"):
    file_handler = logging.FileHandler(path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler

def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler

def get_logger(name):
    set_os_paths()
    config = read_config()
    loglevel = config['logger']['level']
    logger = logging.getLogger(name)
    logpath = config['logger']['path']
    if(loglevel == '20'):
        logger.setLevel(logging.INFO)
    elif(loglevel == '10'):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.NOTSET)
    logger.addHandler(get_file_handler(logpath))
    #logger.addHandler(get_stream_handler())
    return logger