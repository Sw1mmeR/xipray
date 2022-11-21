#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
import os

from xipraylib.xapi_logger import get_logger
from xipraylib.files_holder import is_sudo, set_os_paths, programm_name, install
from xipraylib.xstdout import print_param

logger = get_logger(__name__)

if (__name__ == '__main__'):
    logger.info('Starting script installation')
    
    #os.system('./install/install.sh')
    try:
        is_sudo()
    except Exception as ex:
        print_param(ex, mode='error')
        exit(10)
    set_os_paths()
    install()