from io import StringIO
import os
import json

from censys.common.exceptions import CensysAPIException
from censys.search import CensysHosts
from xipraylib.xapi_logger import get_logger
from xipraylib.files_holder import read_config
from xipraylib.files_holder import censys_results_path
from xipraylib.xstdout import *

logger = get_logger(__name__)

class Censys_api:
    def __init__(self) -> None:
        config = read_config()
        os.environ["CENSYS_API_ID"] = config['Censys']['token']
        os.environ["CENSYS_API_SECRET"] = config['Censys']['secret']
        self.write_path = censys_results_path

    def host_search(self, query):
        logger.info('Start host censys search')
        try:
            censys_hosts = CensysHosts()
            censys_query = censys_hosts.search(query, per_page=5)
            results = censys_query()
            
            with open('test.json', 'w') as file:
                    json.dump(results, file)
            
            tmp_stdout = sys.stdout
            services = StringIO()
            sys.stdout = services

            print_param('Port', results[0]['services'][0]['port'], mode='subtype')

            sys.stdout = tmp_stdout
            result_string = services.getvalue()

            print_host_banner(results[0]['ip'] ,[
                        ('Services', result_string),

                        #('Port', results[0]['services'][0]['port']),
                        #('Service Name', results[0]['services'][0]['service_name']),
                        #('Transport', results[0]['services'][0]['transport_protocol']),

                        ('Country', results[0]['location']['country']),
                        ('City', results[0]['location']['city']),
                        ('Last updated at', results[0]['last_updated_at']),])
        except CensysAPIException as ex:
            logger.error(ex)
            print_param(ex, mode='error')
        except Exception as ex:
            logger.error('Error in shodan search module')
            print_param(ex, mode='error')