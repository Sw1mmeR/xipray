#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from xipraylib.xapi_logger import get_logger
from xipraylib.files_holder import is_sudo, set_os_paths, install
from xipraylib.xstdout import print_param
from sys import platform

logger = get_logger(__name__)

if(__name__ == '__main__'):
    logger.info('Starting script installation')
    
    try:
        if(platform == "linux" or platform == "linux2"):
            logger.info('Linux system detected')
            is_sudo()
            os.system('./install.sh')
        elif(platform == 'win32'):
            logger.info('Windows system detected')
            os.system('./install.bat')
    except Exception as ex:
        print_param(ex, mode='error')
        exit(10)
    set_os_paths()
    install()
    logger.info('Installation finished')