import ipaddress
from webbrowser import get
from xipraylib.xapi_logger import get_logger
from xipraylib.xstdout import *
from xipraylib.files_holder import check_path

logger = get_logger(__name__)

def check_ip(addr, is_print=True):
    if(addr is None):
        logger.debug('Entered addr is None')
        return False
    try:
        ip = ipaddress.ip_address(addr)
        if(is_print):
            print_param(f'{ip} is a correct IPv{ip.version} address', mode='warning')
        logger.debug(f'{ip} is a correct IP {ip.version} address')
        return True
    except ValueError:
        if(is_print):
            print_param(f'Address/netmask is invalid: {addr}', mode='error')
        logger.error(f'Address/netmask is invalid: {addr}')
        return False
    except:
        if(is_print):
            print('[?] Usage : -ip {addr}')
        return False

def check_ip_or_path(value, is_print=False):
    is_ip = check_ip(value, is_print=is_print)
    is_path = check_path(value, is_print=is_print)
    logger.info(f'Checking input ip or path. Is ip: {is_ip}. Is path: {is_path}')
    return is_ip or is_path

def check_boolean(value: str):
    if(value == 'true' or value == 'True'):
        return True
    elif(value == 'false' or value == 'False'):
        return False
    else:
        raise ValueError(f'Incorrect value {value}. Set only boolean value!')

