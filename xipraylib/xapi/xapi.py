from io import StringIO
from xipraylib.xapi.shodan_api import Shodan_api
from xipraylib.xapi.censys_api import Censys_api
from xipraylib.xapi_validator import check_ip
from xipraylib.xstdout import print_host_banner

class Xapi:
    def __init__(self, is_shodan, is_censys) -> None:
        self.out = StringIO()
        self.shodan = Shodan_api(out=self.out) if is_shodan else None
        self.censys = Censys_api(out=self.out) if is_censys else None
        self.results = []

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
        #print(self.results)
        print_host_banner(ip, self.results)

