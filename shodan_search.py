from requests.models import RequestField
import shodan
import requests
import colored
import requests
import json
from files_holder import read_config
from progress.bar import ShadyBar
import time
import logging

logger = logging.getLogger(__name__)

_parameters = {
    'country' : 'country_name',
    'city' : 'city',
    'geo' : 'coords'
}

bar = ShadyBar('Parsing', max=100, suffix='%(percent)d%%')

def _parse_prameters(param):
    try:
        splitted = param.split(' ')
        query = splitted[0]
        result_params = list()
        for line in splitted:
            result_params.append(line)         
        
        logger.info(query)

    except Exception as ex:
        logger.error(ex)
    pass

def search(token, data):
    shodan_api = shodan.Shodan(token)
    #_parse_prameters(data)
    try:
        results = shodan_api.search(data)

        with open('results.json', 'w+') as file:
            json.dump(results, file)

        if (results['total'] == 0):
            logger.info('No matches found!')
            print('No matches found!')
            return None
        else:
            if(results['total'] < 100):
                bar.max = results["total"]
            logger.info(f'Founded: {results["total"]}')
            return results
    except shodan.APIError as ex:
        logger.error(f'Shodan api error: {ex}')
    except Exception as ex:
        logger.error(ex)

def get_by_location(token, query, location: str):
    results = search(token, query)
    resuls_addr = list()
    addr = ''
    if results is not None:
        for result in results['matches']:
            for field in result['location']:
                if (result['location']['city'] == location):
                    if(result['ip_str'] not in resuls_addr):
                        resuls_addr.append(result['ip_str'])
                        logger.info(result['ip_str'])
                        logger.debug(f'City matching found')
                elif (result['location']['country_name'] == location):
                    if(result['ip_str'] not in resuls_addr):
                        resuls_addr.append(result['ip_str'])
                        logger.info(result['ip_str'])
                        logger.debug('Country name matching found')
                elif (result['location']['country_code'] == location):
                    if(result['ip_str'] not in resuls_addr):
                        resuls_addr.append(result['ip_str'])
                        logger.info(result['ip_str'])
                        logger.debug('County code matching found')
                elif (result['location']['latitude'] == location.split(' ')[0] and result['location']['longitude'] == location.split(' ')[1]):
                    if(result['ip_str'] not in resuls_addr):
                        resuls_addr.append(result['ip_str'])
                        logger.info(result['ip_str'])
                        logger.debug('Coordinates matching found')
            bar.next()
            time.sleep(0.02)
    return resuls_addr




