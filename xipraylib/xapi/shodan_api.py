import json
import shodan

from xipraylib.files_holder import read_config
from xipraylib.xstdout import *
from xipraylib.xapi_logger import get_logger

logger = get_logger(__name__)

class Shodan_api:
    def __init__(self) -> None:
        config = read_config()
        shodan_key = config["Shodan"]["token"]
        self.api = shodan.Shodan(shodan_key)
        logger.info('Init shodan search')
        self.popular_ports = [7, 20, 21, 22, 23, 25, 80, 443, 8080]
        
    def host_search(self, query):
        logger.info('Start host shodan search')
        start_service_message('Shodan')
        try:
            results = self.api.host(query)
            with open('test.json', 'w') as file:
                json.dump(results, file) #, sort_keys = True
            logger.info('Sorting ports list')
            ports_list = sorted(results['ports'], key=lambda x: x - 1000000 if x in self.popular_ports else x)
            if('vulns' in results):
                vulns = results['vulns']
            else:
                vulns = 'Not detected'
            return (results['ip_str'], [
                    ('Hostnames', ''.join(results['hostnames'])),
                    ('OS', results['os']),
                    ('Country', results['country_name']),
                    ('City', results['city']),
                    ('Organization', results['org']),
                    ('Ports', ports_list),
                    ('Vulnerabilities', vulns)
                    ])
        except shodan.exception.APIError as ex:
            logger.error(ex)
            print_param(ex, mode='error')
        except Exception as ex:
            logger.error('Error in shodan search module')
            print_param(ex, mode='error')
    
    def domain_search(self, query):
        logger.info('Start domain shodan search')
        start_service_message('Shodan')
        try:
            results = self.api.dns.domain_info(query)
            with open('test.json', 'w') as file:
                json.dump(results, file) #, sort_keys = True
            '''
            logger.info('Sorting ports list')
            ports_list = sorted(results['ports'], key=lambda x: x - 1000000 if x in self.popular_ports else x)
            if('vulns' in results):
                vulns = results['vulns']
            else:
                vulns = 'Not detected'
            return (results['ip_str'], [
                    ('Hostnames', ''.join(results['hostnames'])),
                    ('OS', results['os']),
                    ('Country', results['country_name']),
                    ('City', results['city']),
                    ('Organization', results['org']),
                    ('Ports', ports_list),
                    ('Vulnerabilities', vulns)
                    ])
            '''
        except shodan.exception.APIError as ex:
            logger.error(ex)
            print_param(ex, mode='error')
        except Exception as ex:
            logger.error('Error in shodan search module')
            print_param(ex, mode='error')