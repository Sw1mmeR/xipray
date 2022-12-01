import datetime
import sys
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
    #print(f'{current_time.strftime("%Y/%m/%d %H:%M:%S")} Starting xIPray')
    #print('=' * line_count)

def start_service_message(message):
    current_time = datetime.datetime.now()
    print('=' * line_count)
    print(f'{current_time.strftime("%Y/%m/%d %H:%M:%S")} Starting {message}')
    print('=' * line_count)

def start_censys():
    pass

def print_param(name, value = None, mode='info', file=sys.stdout, max_list_size=5):
    from xipraylib.files_holder import results_path
    #for row in data:
        #print "".join(word.ljust(col_width) for word in row)
    if(mode == 'info' and value is not None):
        if(type(value) == list and file == sys.stdout):
            if(len(value) > max_list_size):
                try:
                    try_parse = int(value[0])
                    print('[+] {0:20}:{1}* More in {2}'.format(name, value[0:max_list_size], results_path))
                except ValueError as ex:
                    print('[+] {0:20}:{1}'.format(name, value[0]))
                    empty = ''
                    for i in range(1, max_list_size):
                        print('[*] {0:20}:{1}'.format(empty, value[i]))
                    print('[*] {0:20}:{1}'.format(empty, f'More in {results_path}'))
                #print('[+] {0:20}:{1}* More in {2}'.format(name, value[0:max_list_size], results_path))
            else:
                print('[+] {0:20}:{1}'.format(name, value[0:max_list_size]))
        else:
            print('[+] {0:20}:{1}'.format(name, value), file=file)
    elif(mode == 'error'):
        print(f'\033[31m[!] {name}\033[0m', file=file)
    elif(mode == 'warning'):
        print(f'\033[32m[!] {name}\033[0m', file=file)
    elif(value is not None):
        raise ValueError(f'Wrong mode value: {mode}. You can use info/error/warning')

def print_params(parameters: list, file=sys.stdout):
    print('=' * line_count, file=file)
    for param in parameters:
        print_param(param[0], param[1], file=file)
    print('=' * line_count, file=file)

def read_params(config) -> list:
    params = [
        ('Shodan', config['XIP']['Shodan']),
        ('Censys', config['XIP']['Censys']),
        ('Shodan-Token', config['Shodan']['token']),
        ('Censys-Token', config['Censys']['token']),
        ('Censys-Secret', config['Censys']['secret']),
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

def print_host_banner(addr, params: list, file=sys.stdout):
    new_line_count = int((line_count - len(addr) - 1) / 2)
    print(file=file)
    header = '{0}|{1}|{2}'.format('-' * new_line_count, addr, '-' * new_line_count)
    print(header, file=file)
    print_params(params, file=file)
    print(file=file)