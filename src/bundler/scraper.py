__author__ = 'umidqssh'

import urllib2
import bs4

class Scraper:
    def __init__(self, port):
        self.port = port
        response = urllib2.urlopen(self.url())
        soup = bs4.BeautifulSoup(response.read())
        div = soup.find(id="version")
        self.prefix = div.h3.string.split(':')[1].lstrip()
        if len(self.prefix) > 1 and len(self.port) > 1:
            good = True
        else:
            good = False

#scrapping CADDIES url + port
    def url(self):
        return "http://192.168.52.61:" + str(self.port)

#scrapping wrapper sequence
    def scrapePrefix(self):
        if self.prefix == None:
            response = urllib2.urlopen(self.url())
            soup = bs4.BeautifulSoup(response.read())
            div = soup.find(id="version")
            self.prefix = div.h3.string.split(':')[1].lstrip()

#getting files from CADDIES
    def getQlist(self):
        response = urllib2.urlopen(self.url() + '/ddi3instance/qlist')
        return response.read()

    def getSlist(self):
        response = urllib2.urlopen(self.url() + '/ddi3instance/slist')
        return response.read()

    def getIndexhtm(self):
        response = urllib2.urlopen(self.url() + '/ddi3instance/doc')
        return response.read()

    def getddixml(self):
        response = urllib2.urlopen(self.url() + '/ddi3instance/xmlrepo')
        return response.read()
