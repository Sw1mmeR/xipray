import os
import configparser
import logging
from sys import platform
from subprocess import check_output

programm_name = 'xIPray'

config_path = '/'
log_path = '/'
logger = logging.getLogger(__name__)

def check_paths(paths: list):
    for path in paths:
        if not os.path.isdir(path):
            os.mkdir(path)

def is_sudo():
    username = check_output(['whoami']).decode().strip()
    if(username != 'root'):
        raise Exception(f'Current user is {username}, must be root. Use sudo to run this script!')

def __set_logger(path):
    logging.basicConfig(filename=path, level=logging.DEBUG)

def set_os_paths():
    global config_path, log_path
    if platform == "linux" or platform == "linux2":
        # linux
        config_path = f'/etc/{programm_name}/'
        log_path = f'/var/log/{programm_name}/'
        try:
            is_sudo()
        except Exception as ex:
            print(ex)
            exit(10)
        
    elif platform == "darwin":
        # OS X
        pass
    elif platform == "win32":
        # Windows
        config_path = os.path.expanduser("~/Documents") + f'/{programm_name}/'
        log_path = os.path.expanduser("~/Documents") + f'/{programm_name}/'
    check_paths([config_path, log_path])
    __set_logger(log_path + f'{programm_name}.log')

# Ниже можно использовать логер

def read_config(path: str = config_path):
    path_append_filename = config_path + 'config.ini'

    logger.debug(f'Reading config {path_append_filename}')
    
    if not os.path.exists(path_append_filename):
        create_config(path_append_filename)
    config = configparser.ConfigParser()
    config.read(path_append_filename)
    logger.debug(config['Shodan']['token'])
    return config

def create_config(path: str = config_path):
    logger.debug(f'Creating config {path}')
    
    config = configparser.ConfigParser()
    config.add_section("Shodan")
    config.add_section('logger')
    config.set("Shodan", "token", "vIt7JM53a1WJGZ54uaqMtgrm4lXXq8RF")
    config.set('logger', 'level', '10')
    with open(path, "w") as config_file:
        config.write(config_file)