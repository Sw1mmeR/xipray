import datetime
import time
#from columnar import columnar

# Приветсвтенное сообщение/лого
def start_message(parameters: list):
    print('===============================================================')
    print('xIPray v0.3 Alpha')
    print('By KotFedot21 & Sw1mmeR')
    print_params(parameters=parameters)
    current_time = datetime.datetime.now()
    print(f'{current_time.strftime("%Y/%m/%d %H:%M:%S")} Starting xIPray')
    print('===============================================================')

def print_param(name, value = None, type = "info"):
    
    #for row in data:
        #print "".join(word.ljust(col_width) for word in row)
    if(type == 'info'):
        print('[+] {0:20}:{1}'.format(name, value))
    elif(type == 'warning'):
        print(f'[!] {name}')

def print_params(parameters: list):
    print('===============================================================')
    for param in parameters:
        print_param(param[0], param[1])
    print('===============================================================')

def read_params(config) -> list:
    params = [
        ('Shodan', config['XIP']['Shodan']),
        ('ZoomEy', config['XIP']['ZoomEy']),
        ('Censys', config['XIP']['Censys']),
        ('Shodan-Token', config['Shodan']['token']),
        ('ZoomEy-Token', config['ZoomEy']['token']),
        ('Censys-Token', config['Censys']['token']),
        ('Log level', config['logger']['level']),
        ('Log path', config['logger']['path'])
        ]
    return params
