import requests
from xapi_logger import get_logger
import logging

logger = logging.getLogger(__name__)

class Xapi():
    def __init__(self, shoadn_key, censys_key=None, proxy=None) -> None:
        self._base_shodan_url = 'https://api.shodan.io'
        self._base_shodan_key_url = '?key={shoadn_key}'
        if censys_key is not None:
            self._censys_key = censys_key
            self._base_censys_url = ''
            self._base_censys_key_url = ''
        
        self._services = {
        'shodan' : 'https://api.shodan.io',
        'censys' : 'https://search.censys.io/api'
        }
        
        self._actions = {
            'host' : '/shodan/host/'
        }
    
    def request(self, action: str, parameters, service='shodan', method='get'):
        base_url = ''
        if (service in self._services):
            base_url = self._services[service]
        if (action in self._actions):
            base_url += self._actions[action]
        base_url += str(parameters)
        base_url += self._base_shodan_key_url
        logger.debug(f'Set base url {base_url}')

        #_base_shodan_key_url
        



    