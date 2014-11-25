import random
import requests
class ConnectionManager:
    def __init__(self, proxyFile, userAgentFile = r"useragents.txt"):
        self.proxyFile = proxyFile
        self.userAgentFile = userAgentFile
        self._loadData()

    def _loadData(self):
        if self.userAgentFile:
            with open(self.userAgentFile, "r") as f:
                self.userAgents = [l for l in (line.strip() for line in f) if l]
        else:
            self.userAgents = (
    # Top most popular browsers in my access.log on 2009.02.12
    # tail -50000 access.log |
    #  awk -F\" '{B[$6]++} END { for (b in B) { print B[b] ": " b } }' |
    #  sort -rn |
    #  head -20
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.6) Gecko/2009011912 Firefox/3.0.6',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.48 Safari/525.19',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
    'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.5) Gecko/2008121621 Ubuntu/8.04 (hardy) Firefox/3.0.5',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
)
        if self.proxyFile:
            with open(self.proxyFile, "r") as f:
                self.proxies = [l.split(":") for l in (line.strip() for line in f) if l]
        else:
            self.proxies = []

    def getRandomUserAgent(self):
        return random.choice(self.userAgents)

    def getRandomProxy(self):
        if len(self.proxies) == 0: return None
        temp = random.choice(self.proxies)
        if len(temp) == 4:
            return "http://" + temp[2] + ":" + temp[3] + "@" + temp[0] + ":" + temp[1]
        elif len(temp) == 2:
            return "http://" + temp[0] + ":" + temp[1]
        else:
            return None

    def getSessionObject(self):
        headers =  {'User-Agent':self.getRandomUserAgent(),
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
                    }
        proxy = {'http':self.getRandomProxy()}
        s = requests.Session()
        s.headers= headers
        s.proxies = proxy
        s.timeout = 20
        return s

