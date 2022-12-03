import os
from io import StringIO
from xipraylib.xapi.shodan_api import Shodan_api
from xipraylib.xapi.censys_api import Censys_api
from xipraylib.xapi_validator import check_ip
from xipraylib.xstdout import print_host_banner
from xipraylib.files_holder import results_path

class Xapi:
    def __init__(self, is_shodan, is_censys) -> None:
        self.shodan = Shodan_api() if is_shodan else None
        self.censys = Censys_api() if is_censys else None
        self.results = []
        self.write_path = results_path
        if(os.path.isfile(self.write_path)):
            os.remove(self.write_path)

    def host_search(self, value):
        if(check_ip(value, is_print=False)):
            if(self.shodan is not None):
                self.shodan_result = self.shodan.host_search(value)
            if(self.censys is not None):
                self.censys_result = self.censys.host_search(value)
        if(self.shodan is None):
            ip = self.censys_result[0]
            self.results = self.censys_result[1]
        elif(self.censys is None):
            ip = self.shodan_result[0]
            self.results = self.shodan_result[1]
        else:
            ip = self.shodan_result[0]
            self.results = self.shodan_result[1]
            self.results += self.censys_result[1]
        print_host_banner(ip, self.results)
        with open(self.write_path, 'a') as file:
            print_host_banner(ip, self.results, file=file)