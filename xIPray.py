#!/usr/bin/python3
# -*- coding: utf-8 -*-

import configparser
import argparse
import logging
from files_holder import *
import shodan_search
from ipaddress import ip_address
from art import tprint
from xapi import Xapi
from xapi_logger import get_logger

parser = argparse.ArgumentParser(description='White Hat hack tool. Enjoy.')

logger = get_logger(__name__)

# Приветсвтенное сообщение/лого
def welcome_message():
    tprint('xIPray', font='big')
    tprint("Hack your a$$", font='small')

def args_init():
    #parser.add_argument('-shodan', type=str, help='Use shodan search')
    #parser.add_argument('-censys', type=str, help='Use censys search')
    parser.add_argument('search', type=str, help='String to search')
    parser.add_argument('-location', '-l', type =str, help='Host location') #action='store_true'
    parser.add_argument('-filter', '-f', action='store_true', help='Use filters')
def main():
    #welcome_message()
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

    #shodan_search.search(config['Shodan']['token'], search_str)

if (__name__ == '__main__'):
    main()