import json
import os
import shodan

from xipraylib.files_holder import read_config
from xipraylib.xstdout import *
from xipraylib.xapi_logger import get_logger
from xipraylib.xapi_validator import check_ip

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
            print_host_banner(results['ip_str'] ,[
                    ('Hostnames', ''.join(results['hostnames'])),
                    ('OS', results['os']),
                    ('Country', results['country_name']),
                    ('City', results['city']),
                    ('Organization', results['org']),
                    ('Ports', ports_list),
                    ('Vulnerabilities', vulns)
                    ], file=self.out)
            '''with open(self.write_path, 'a') as file:
                print_host_banner(results['ip_str'] ,[
                    ('Hostnames', ''.join(results['hostnames'])),
                    ('OS', results['os']),
                    ('Country', results['country_name']),
                    ('City', results['city']),
                    ('Organization', results['org']),
                    ('Ports', ports_list),
                    ('Vulnerabilities', vulns)
                    ], file=self.out)'''
            return self.out.getvalue()
        except shodan.exception.APIError as ex:
            logger.error(ex)
            print_param(ex, mode='error')
        except Exception as ex:
            logger.error('Error in shodan search module')
            print_param(ex, mode='error')

    def multi_host_search(self, path):
        test = StringIO()
        with open(path) as file:
            for addr in file:
                clean_addr = addr.strip()
                if(check_ip(clean_addr)):
                    self.host_search(clean_addr)
                else:
                    print_param(f'Skip {clean_addr}', mode='error', file=test)
        print(test)
        return test.getvalue()