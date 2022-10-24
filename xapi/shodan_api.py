import json
from files_holder import read_config
import shodan
from xstdout import *
from xapi_logger import get_logger

logger = get_logger(__name__)

class Shodan_api:
    def __init__(self) -> None:
        config = read_config()
        shodan_key = config["Shodan"]["token"]
        self.api = shodan.Shodan(shodan_key)
        logger.info('Init shodan search')

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
        except shodan.exception.APIError as ex:
            logger.error(ex)
            print_param(ex, type='error')
        except Exception as ex:
            logger.error('Error in shodan search module')
            print_param(ex, type='error')

    def search_vulnerable_cam_router(self):
        res = self.api.search(query='WIRELESS+INTERNET+CAMERA city:Moscow')
        print(res)
        pass
