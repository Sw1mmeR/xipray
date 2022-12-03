from io import StringIO
import os
import json

from censys.common.exceptions import CensysAPIException
from censys.search import CensysHosts
from xipraylib.xapi_logger import get_logger
from xipraylib.files_holder import read_config
from xipraylib.xstdout import *
from xipraylib.xapi_validator import check_ip

logger = get_logger(__name__)

class Censys_api:
    def __init__(self) -> None:
        config = read_config()
        os.environ["CENSYS_API_ID"] = config['Censys']['token']
        os.environ["CENSYS_API_SECRET"] = config['Censys']['secret']

    def host_search(self, query):
        logger.info('Start host censys search')
        start_service_message('Censys')
        try:
            censys_hosts = CensysHosts()
            censys_query = censys_hosts.search(query, per_page=5)
            results = censys_query()
            if(len(results) == 0):
                print_param('No information available for that IP.', mode='error')
                return
            
            with open('test.json', 'w') as file:
                    json.dump(results, file)
            
            services = ''
            for i in range(0, len(results[0]['services'])):
                port = print_param('Port', results[0]['services'][i]['port'], mode='subtype')
                name = print_param('Service Name', results[0]['services'][i]['service_name'], mode='subtype')
                transport = print_param('Transport', results[0]['services'][i]['transport_protocol'], mode='subtype')
                services += '\n' + port + '\n' + name + '\n' + transport
            return (results[0]['ip'] ,[
                ('Services', services),
                ('Last updated at', results[0]['last_updated_at'])
                ])
            print_host_banner(results[0]['ip'] ,[
                        ('Services', services),
                        #('Country', results[0]['location']['country']),
                        #('City', results[0]['location']['city']),
                        ('Last updated at', results[0]['last_updated_at']),
                        ],file=self.out)
            '''
            with open(self.write_path, 'a') as file:
                print_host_banner(results[0]['ip'] ,[
                        ('Services', services),
                        ('Country', results[0]['location']['country']),
                        ('City', results[0]['location']['city']),
                        ('Last updated at', results[0]['last_updated_at']),
                        ],file=self.out)
                        '''
            return self.out.getvalue()
        #except CensysAPIException as ex:
            #logger.error(ex)
            #print_param(ex, mode='error')
        except Exception as ex:
            logger.error('Error in censys search module')
            print_param(ex, mode='error')
            
    def multi_host_search(self, path):
        with open(path) as file:
            for addr in file:
                clean_addr = addr.strip()
                if(check_ip(clean_addr)):
                    self.host_search(clean_addr)
                else:
                    print_param(f'Skip {clean_addr}', mode='error')