import os
from xipraylib.xapi.shodan_api import Shodan_api
from xipraylib.xapi.censys_api import Censys_api
from xipraylib.xapi_validator import check_ip
from xipraylib.xstdout import print_host_banner, print_param
from xipraylib.files_holder import results_path

class Xapi:
    def __init__(self, is_shodan, is_censys, is_file) -> None:
        self.shodan = Shodan_api() if is_shodan else None
        self.censys = Censys_api() if is_censys else None
        self.is_file = is_file
        self.results = []
        self.write_path = results_path
        self.shodan_result = None
        self.censys_result = None
        if(os.path.isfile(self.write_path)):
            os.remove(self.write_path)

    def host_search(self, value):
        if(check_ip(value, is_print=False)):
            if(self.shodan is not None):
                self.shodan_result = self.shodan.host_search(value)
            if(self.censys is not None):
                self.censys_result = self.censys.host_search(value)
        else:
            self.shodan.domain_search(value)
        if(self.censys_result is None and self.shodan_result is None):
            return
        if(self.shodan is None and self.censys_result is not None):
            ip = self.censys_result[0]
            self.results = self.censys_result[1]
        elif(self.censys is None and self.shodan_result is not None):
            ip = self.shodan_result[0]
            self.results = self.shodan_result[1]
        else:
            ip = self.shodan_result[0] if self.shodan_result is not None else self.censys_result[0]
            self.results = self.shodan_result[1] if self.shodan_result is not None else self.censys_result[1]
            if(self.censys_result is not None):
                self.results += self.censys_result[1]
        if (self.is_file):
            with open(self.write_path, 'a') as file:
                print_host_banner(ip, self.results, file=file)
        else:
            print_host_banner(ip, self.results)
    
    def multi_host_search(self, path):
        with open(path) as file:
            for addr in file:
                clean_addr = addr.strip()
                if(check_ip(clean_addr)):
                    self.host_search(clean_addr)
                else:
                    print_param(f'Skip {clean_addr}', mode='error')