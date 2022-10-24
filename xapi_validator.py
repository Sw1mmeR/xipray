import ipaddress
from webbrowser import get
from xapi_logger import get_logger
from xstdout import *

logger = get_logger(__name__)

def check_ip(addr):
    if(addr is None):
        logger.debug('Entered addr is None')
        return
    try:
        ip = ipaddress.ip_address(addr)
        print_param(f'{ip} is a correct IPv{ip.version} address {addr}', type='warning')
        logger.debug(f'{ip} is a correct IP {ip.version} address')
        return True
    except ValueError:
        print_param(f'Address/netmask is invalid: {addr}', type='error')
        logger.error(f'Address/netmask is invalid: {addr}')
        return False
    except:
        print('[?] Usage : -ip {addr}')
        return False