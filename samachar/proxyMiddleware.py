import scrapy
import random
import logging
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

class ProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, proxy_ip=''):
        self.proxy_ip = proxy_ip

    def process_request(self,request,spider):
        ip = random.choice(self.proxy_list)
        if ip:
            request.meta['proxy']= ip
            spider.log('proxy-ip: {} {}'.format(request.meta['proxy'], request))
   
    '''def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
        p = random.choice(PROXIES)
        try:
            request.meta['proxy'] = "http://%s" % p
        except Exception, e:
            log.msg("Exception %s" % e, _level=log.CRITICAL)'''

    def process_exception(self, request, exception, spider):
        url = request.url
        proxy = request.meta['proxy']
        myfile = open('outurl_excep.txt','a')
        myfile.write(url+'\n')
        myfile.write(proxy+'\n')
        myfile.close()

    proxy_list = [\
        "https://198.169.246.30:80",\
	    "https://175.43.123.1:55336",\
	    "https://175.43.123.1:55336",\
        "http://24.173.40.24:8080",\
        "https://180.76.135.145:3128",\
        "https://137.116.76.252:3128",\
        "https://222.88.236.236:80",\
        "https://190.98.162.22:8080",\
        "https://168.63.24.174:8118",\
        "https://84.124.11.207:3128",\
        "https://213.208.177.124:3128",\
        "https://200.180.32.58:80",\
        "https://200.180.32.58:80",\
        "http://61.191.27.117:443",\
        "https://186.93.171.48:8080",\
        "https://94.245.176.141:3128",\
        "https://189.38.71.130:80",\
        "https://45.32.161.29:8080",\
        "https://92.96.157.128:8118",\
        "https://92.99.205.44:8118",\
        "https://62.176.13.22:8088",\
        #"https://77.120.224.229:3128",\
        #"https://186.42.226.4:8080",\
        #"https://94.245.176.141:3128",\
        #"https://183.111.169.202:3128",\
        #"https://122.193.14.105:83",\
        #"https://117.136.234.6:843",\
        #"https://116.231.214.213:8118",\
        #"https://107.151.136.197:80",\
        #"https://122.96.59.107:843",\
        #"https://199.227.40.31:80",\
        #"https://107.151.136.197:80",\
        #"https://107.151.152.218:80",\
        #"https://201.72.254.82:80",\
        #"https://138.201.0.109:3128",\
        #"https://137.135.166.225:8129",\
        #"https://167.114.195.242:3128",\
        #"https://212.74.214.189:3128", 
        #"https://136.243.197.251:3128",\
        #"https://168.63.24.174:8126",
        #"https://108.59.10.135:55555",\
        #"https://117.131.216.214:80",\
        #"https://125.90.207.93:80",\
        #"https://203.66.159.46:3128",\
        #"https://52.90.246.152:8083",
        #"https://117.131.216.214:80",\
        #"https://111.161.126.108:80",\
        #"https://149.91.81.62:8080",\
        #"https://108.59.10.135:55555",\
        #"https://149.91.81.62:8080",\
        #"https://101.200.179.38:3128",\
        #"https://195.138.87.63:3128",\
        #"https://190.147.220.37:8080",
        #"https://178.62.44.72:80",\
        #"https://219.255.197.90:3128",\
        #"https://183.207.232.43:80",\
        #"https://91.235.91.62:3128",\
        #"https://31.168.236.236:8080",\
        #"https://31.207.0.99:3128",\
        #"https://108.59.10.129:55555",
        #"https://185.28.193.95:8080",\
        #"https://122.226.166.231:8080",\
        #"https://94.59.171.203:8118",\
        #"https://31.207.0.99:3128",\
        #"https://46.97.103.50:3128",\
        #"https://176.65.43.137:3128",\
        #"https://91.121.132.52:8080",\
        #"https://210.96.153.20:3128",\
        #"https://63.150.152.151:3128",\
        #"https://221.176.14.72:80",
        #"https://184.49.233.234:8080",\
        #"https://137.135.166.225:8121",\
        #"https://137.135.166.225:8146",\
        #"https://168.63.20.19:8120",\
        #"https://168.63.20.19:8125",				  
				  
         
	#"socks4/5://166.62.97.244:18628",\
	#"socks4/5://223.252.38.195:600881"
    ]

