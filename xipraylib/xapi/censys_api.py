import os
import json

from censys.search import CensysHosts
from xipraylib.xapi_logger import get_logger
from xipraylib.files_holder import read_config
from xipraylib.files_holder import censys_results_path

logger = get_logger(__name__)

class Censys_api:
    def __init__(self) -> None:
        config = read_config()
        os.environ["CENSYS_API_ID"] = config['Censys']['token']
        os.environ["CENSYS_API_SECRET"] = config['Censys']['secret']
        self.write_path = censys_results_path

    def host_search(self, query):
        logger.info('Start host censys search')
        censys_hosts = CensysHosts()
        censys_query = censys_hosts.search(query, per_page=5)
        results = censys_query()

        with open(self.write_path, 'w') as file:
                json.dump(results, file)
        print(results)