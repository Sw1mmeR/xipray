import imp
import json
import os
from xipraylib.files_holder import check_path, read_config
import shodan
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
        self.write_path = './host_search_results.txt'
        if(os.path.isfile(self.write_path)):
            os.remove(self.write_path)

    def host_search(self, query):
        logger.info('Start host shodan search')
        try:
            results = self.api.host(query)
            with open('test.json', 'w') as file:
                json.dump(results, file) #, sort_keys = True
            print_host_banner(results['ip_str'] ,[
                    ('Hostnames', ''.join(results['hostnames'])),
                    ('OS', results['os']),
                    ('Country', results['country_name']),
                    ('City', results['city']),
                    ('Organization', results['org']),
                    ('Ports', results['ports'])
                    ])
            with open(self.write_path, 'a') as file:
                print_host_banner(results['ip_str'] ,[
                    ('Hostnames', ''.join(results['hostnames'])),
                    ('OS', results['os']),
                    ('Country', results['country_name']),
                    ('City', results['city']),
                    ('Organization', results['org']),
                    ('Ports', results['ports'])
                    ], file=file)
        except shodan.exception.APIError as ex:
            logger.error(ex)
            print_param(ex, mode='error')
        except Exception as ex:
            logger.error('Error in shodan search module')
            print_param(ex, mode='error')

    def multi_host_search(self, path):
        with open(path) as file:
            for addr in file:
                clean_addr = addr.strip()
                if(check_ip(clean_addr)):
                    self.host_search(clean_addr)
                else:
                    print_param(f'Skip {clean_addr}', mode='error')

    def search_vulnerable_cam_router(self):
        res = self.api.search(query='WIRELESS+INTERNET+CAMERA city:Moscow')
        print(res)
        pass