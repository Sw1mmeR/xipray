#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
import configparser
import argparse
import logging
from files_holder import *
from ipaddress import ip_address
from xapi_logger import get_logger
from xstdout import *
from xapi.shodan_api import Shodan_api
from xapi_validator import *

parser = argparse.ArgumentParser(description='White Hat hack tool. Enjoy.')
subparsers = parser.add_subparsers(help='Script commands for change arguments')
set_subparser = subparsers.add_parser('set', help='Set parametr value')
#ip_subparser = subparsers.add_parser('ip', help='Target ip addr')
logger = get_logger(__name__)

params_list = ['shodan', 'zoomey', 'censys', 'Shodan-Token', 'ZoomEy-Token', 'Censys-Token', 'loglevel', 'logpath']

def args_init():
    group = set_subparser.add_mutually_exclusive_group(required=True)
    group.add_argument('-shodan', type=bool, help='Enable or disable Shodan search')
    group.add_argument('-zoomey', type=bool, help='Enable or disable ZoomEy search')
    group.add_argument('-censys', type=bool, help='Enable or disable Censys search')

    group.add_argument('-shodanToken', help='Your\'s personal Shodan token')
    group.add_argument('-zoomeyToken', help='Your\'s personal ZoomEy token')
    group.add_argument('-censysToken', help='Your\'s personal Censys token')

    group.add_argument('-loglevel', type=int, help='Log level. [10, 20, 30]')
    group.add_argument('-logpath', type=str, help='Path to log file')


    parser.add_argument('-ip', type=str, help='IP addr to search')
    #ip_subparser.add_argument('-scan', '-s', action='store_true', help='Start scanning addr')
    parser.add_argument('-list', '-l', action='store_true', help='Show current configuration')
    #parser.add_argument('set', help='Set parameter. Usage: -set [parameter] [value]')

    #parser.add_argument('-location', '-l', type =str, help='Host location') #action='store_true'
    #parser.add_argument('-filter', '-f', action='store_true', help='Use filters')
def main():
    args_init()
    args = parser.parse_args()
    set_os_paths()
    config = read_config()
    execute = False
    ip_search = False
    ip_file_search = False
    if(hasattr(args, 'shodan') and args.shodan):
        config.set('XIP', 'Shodan', str(args.shodan))
        update_config(config)
    if(hasattr(args, 'zoomey') and args.zoomey):
        config.set('XIP', 'zoomey', str(args.zoomey))
        update_config(config)
    if(hasattr(args, 'censys') and args.censys):
        config.set('XIP', 'censys', str(args.censys))
        update_config(config)
    if(hasattr(args, 'shodanToken') and args.shodanToken):
        config.set('Shodan', 'token', str(args.shodanToken))
        update_config(config)
    if(hasattr(args, 'zoomeyToken') and args.zoomeyToken):
        config.set('ZoomEy', 'token', str(args.zoomeyToken))
        update_config(config)
    if(hasattr(args, 'censysToken') and args.censysToken):
        config.set('Censys', 'token', str(args.censysToken))
        update_config(config)
    if(hasattr(args, 'loglevel') and args.loglevel):
        config.set('logger', 'level', str(args.loglevel))
        update_config(config)
    if(hasattr(args, 'logpath') and args.logpath):
        config.set('logger', 'path', str(args.logpath))
        update_config(config)
    if(args.list):
        params = read_params(config)
        print_params(parameters=params)
        return   
    if(len(sys.argv) == 1):
        parser.print_help()
        sys.exit() 
    if(hasattr(args, 'ip')):
        if(check_ip_or_path(args.ip)):
            execute = True
    if(execute):
        try:
            params = read_params(config)
            start_message(parameters=params)
            shodan_api = Shodan_api()
            if(check_ip(args.ip)):
                shodan_api.host_search(args.ip)
            elif(check_path(args.ip)):
                shodan_api.multi_host_search(args.ip)
            #time.sleep(10)
        except KeyboardInterrupt:
            print_param("CTRL+C detected, terminating.", type="error"),
            sys.exit()
    '''
        args_init()
    args = parser.parse_args()
    set_os_paths()
    # После установки системных путей можно использовать логер
    config = read_config()
    if(args.filter):
        location_result = shodan_search.get_by_location(config['Shodan']['token'], args.search, args.location)
        print()
        print(location_result)
    else:
        shodan_search.search(config['Shodan']['token'], args.search)
    '''

if (__name__ == '__main__'):
    main()