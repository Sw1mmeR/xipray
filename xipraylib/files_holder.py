import os
import configparser
import logging
from sys import platform
from subprocess import check_output
from xipraylib.xstdout import print_param

programm_name = 'xipray'

install_path = '/'
config_path = '/'
log_path = '/'

logger = logging.getLogger(__name__)

def check_paths(paths: list):
    for path in paths:
        if not os.path.isdir(path):
            os.mkdir(path)

def check_path(path, is_print=True):
    if(os.path.isdir(path)):
        if(is_print):
            print_param(f'{path} is a directory' ,mode="error")
        logger.error(f'{path} is a directory')
        return False
    elif(os.path.isfile(path)):
        if(is_print):
            print_param(f'{path} is exist', mode='warning')
        logger.info(f'{path} is exist')
        return True
    else:
        if(is_print):
            print_param(f'Invalid input', mode='error')
        logger.error(f'Invalid input')
        return False

def is_sudo():
    username = check_output(['whoami']).decode().strip()
    if(username != 'root'):
        raise Exception(f'Current user is {username}, must be root. Use sudo to run this script!')

def __set_logger(path):
    logging.basicConfig(filename=path, level=logging.DEBUG)

def set_os_paths():
    global config_path, log_path, install_path
    if platform == "linux" or platform == "linux2":
        # linux
        config_path = f'/etc/{programm_name}/'
        log_path = f'/var/log/{programm_name}/'
        install_path = f'/etc/{programm_name}/'
        try:
            is_sudo()
        except Exception as ex:
            print_param(ex, mode='error')
            exit(10)
        
    elif platform == "darwin":
        # OS X
        pass
    elif platform == "win32":
        # Windows
        config_path = os.path.expanduser("~/Documents") + f'/{programm_name}/'
        log_path = os.path.expanduser("~/Documents") + f'/{programm_name}/'
        install_path = 'C:\\'
    check_paths([config_path, log_path])
    config_path = config_path + 'config.ini'
    __set_logger(log_path + f'{programm_name}.log')

# Ниже можно использовать логер

def read_config(path: str = config_path):
    path_append_filename = config_path

    logger.debug(f'Reading config {path_append_filename}')
    
    if not os.path.exists(path_append_filename):
        create_config(path_append_filename)
    config = configparser.ConfigParser()
    config.read(path_append_filename)
    return config

def update_config(config):
    set_os_paths()
    path = config_path
    logger.debug(f'Updating config {path}')
    with open(path, "w") as config_file:
        config.write(config_file)

def create_config(path: str = config_path):
    if platform == "linux" or platform == "linux2":
        is_sudo()
    config = None
    logger.debug(f'Creating config {config_path}')
    
    config = configparser.ConfigParser()
    config.add_section("XIP")
    config.set("XIP", "Shodan", "True")
    config.set("XIP", "ZoomEy", "False")
    config.set("XIP", "Censys", "False")
        
        #config.set("XIP", "shodan-key", "None")
        #config.set("XIP", "zoomey-key", "None")
        #config.set("XIP", "censys-key", "None")

        #config.set("XIP", "loglevel", "20")
        #config.set("XIP", "logpath", log_path)

    config.add_section("Shodan")
    config.set("Shodan", "token", "None")
    config.add_section("ZoomEy")
    config.set("ZoomEy", "token", "None")
    config.add_section("Censys")
    config.set("Censys", "token", "None")

    config.add_section('logger')
    config.set('logger', 'level', '20')
    config.set('logger', 'path', log_path)
    
    with open(path, "w") as config_file:
        config.write(config_file)

def install():
    logger.info(f'Moving libraries to {install_path}')
    os.system(f'cp -rv xipraylib/ {install_path}')
    os.system(f'cp -v xipray {install_path}')
    os.system(f'chmod +x {install_path}xipray')
    os.system(f'rm /usr/bin/{programm_name}')
    os.system(f'ln -s {install_path}xipray /usr/bin/{programm_name}')