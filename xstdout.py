import datetime
import time
#from columnar import columnar

line_count = 72

# Приветсвтенное сообщение/лого
def start_message(parameters: list):
    print('=' * line_count)
    print('xIPray v0.3 Alpha')
    print('By KotFedot21 & Sw1mmeR')
    print_params(parameters=parameters)
    current_time = datetime.datetime.now()
    print(f'{current_time.strftime("%Y/%m/%d %H:%M:%S")} Starting xIPray')
    print('=' * line_count)


def print_param(name, value = None, type = "info"):
    #for row in data:
        #print "".join(word.ljust(col_width) for word in row)
    if(type == 'info'):
        print('[+] {0:20}:{1}'.format(name, value))
    elif(type == 'error'):
        print(f'\033[31m[!] {name}\033[0m')
    elif(type == 'warning'):
        print(f'\033[32m[!] {name}\033[0m')

def print_params(parameters: list):
    print('=' * line_count)
    for param in parameters:
        print_param(param[0], param[1])
    print('=' * line_count)



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

def print_banner(ip, country, city, count = None):
    print('-' * line_count)
    if(count is not None):
        print(f'Id = {count}')
    print(ip)
    print(f'{country}, {city}')
    print('-' * line_count)

def print_host_banner(addr, params: list):
    new_line_count = int((line_count - len(addr) - 1) / 2)
    
    print()
    header = '{0}|{1}|{2}'.format('-' * new_line_count, addr, '-' * new_line_count)
    print(header)
    print_params(params)
    print()