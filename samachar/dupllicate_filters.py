import os

from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.request import request_fingerprint

class CustomFilter(RFPDupeFilter):
    """A dupe filter that considers specific ids in the url"""
 
    def __getid(self, url):
        #mm = url.split("&refer")[0] #or something like that
    
        #url ='http://www.thebarcodewarehouse.co.uk/labels-and-ribbons/self-adhesive-labels/zebra-labels/800283-205/'
        #url = 'http://www.thebarcodewarehouse.co.uk/search-results/?searchterm=GK42-102520-000+&searchterm_submit=Search'

        if 'searchterm' in url:
            url_list = url.split("=")
            url_list = filter(None, url_list)
            mm = url_list[1]
            #print url_list[1].split("+")[0]
        else:
            url_list = url.split("/")
            url_list = filter(None, url_list)
            mm = url_list[-1]
        return mm

    def request_seen(self, request):
       fp = self.__getid(request.url)
       if fp in self.fingerprints:
           return True
       self.fingerprints.add(fp)
       if self.file:
           self.file.write(fp + os.linesep)