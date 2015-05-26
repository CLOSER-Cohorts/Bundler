__author__ = 'umidqssh'

import urllib2
import bs4
import os
import shutil
from xlrd import open_workbook
from xlwt import Workbook
from xlutils import copy as xl_copy
import csv
import patcher

class Instance:
    def __init__(self, port, root):
        self.port = port
        self.prefix = None
        self.output = os.path.join(root, "..\\output\\")
        self.assets = os.path.join(root, "..\\assets\\")

    def url(self):
        return "http://192.168.52.39:" + str(self.port)

    def scrapePrefix(self):
        if self.prefix == None:
            response = urllib2.urlopen(self.url())
            soup = bs4.BeautifulSoup(response.read())
            div = soup.find(id="version")
            self.prefix = div.h3.string.split(':')[1].lstrip()

    def path(self):
        self.scrapePrefix()
        return self.output + self.prefix + "\\"

    def run(self):
        self.scraper = scraper.Scraper(self.port)
        qlist = scraper.Scraper.getQlist()
        qlist = patcher.Patcher().patchindexhtm(qlist)

#creating bundle folder and resources folder within
    def setupFolders(self):
        self.scrapePrefix()
        if not os.path.exists(self.output + self.prefix):
            os.makedirs(self.output + self.prefix)
        else:
            print 'Bundle folder already created for' + ' ' + self.prefix
        if not os.path.exists(self.path() + 'resources'):
            os.makedirs(self.path() + 'resources')
        else:
            print 'Resources folder already created for' + ' ' + self.prefix

#creating config files
    def configfiles(self):
        files = ['dv.txt','labels.txt','linking.txt','mapping.txt','notes.txt','redactions.txt']
        for i in files:
            if not os.path.exists(self.path() + i):
                file = open(self.path() + i, 'w')
            else:
                print i + ' ' + 'already created'

#downloadables from CADDIES
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

#creating txt files in resources folder
    def writelistfiles(self):
        text = self.getQlist()
        if not os.path.isfile(self.path() + 'resources\qlist.txt'):
            with open(self.path() + 'resources\qlist.txt', 'w') as f:
                f.write(text)
        else:
            print 'qlist.txt already downloaded'
        text2 = self.getSlist()
        if not os.path.isfile(self.path() + 'resources\slist.txt'):
            with open(self.path() + 'resources\slist.txt', 'w') as f:
                f.write(text2)
        else:
            print 'slist.txt already downloaded'

#creating index.htm
    def writeindexhtm(self):
        text = self.getIndexhtm()
        if not os.path.isfile(self.path() + 'index.htm'):
            with open(self.path() + 'index.htm', 'w') as f:
                f.write(self.patchindexhtm(text))
        else:
            print 'index.htm already saved'

#patch for index.htm
    def patchindexhtm(self, text):
        with open(self.assets + '\patch.txt', 'r') as f:
            patch = f.read()
            #with open(self.path() + '\index.htm', 'r+') as w:
            search = '</head>'
                #text = w.read()
            text = text.replace('/stylesheets','index_files').replace('/javascripts','index_files').replace('/images','index_files')
            text = text.replace(search, patch+'\n'+search)
                #w.seek(0)
                #w.truncate()
                #w.write(text)
            return text

#creating ddi.xml
    def writeddixml(self):
        text = self.getddixml()
        if not os.path.isfile(self.path() + 'ddi.xml'):
            with open(self.path() + 'ddi.xml', 'w') as f:
                f.write(text)
        else:
            print 'ddi.xml already saved'

#copying files from TOOLS
    def copymanual(self):
        self.path()
        if not os.path.exists(self.path() + 'Metadata Delivery Bundle.pdf'):
            shutil.copy('C:\CLOSER\Python\\assets\Metadata Delivery Bundle.pdf', self.path())
        else:
             print 'manual already copied'

    def copyfiles(self):
        self.path()
        if not os.path.exists(self.path() + 'CV.txt'):
            shutil.copy('C:\CLOSER\Python\\assets\CV.txt', self.path() + 'resources')
        else:
            print 'CV.txt already copied'
        if not os.path.exists(self.path() + 'linking.xlsx'):
            shutil.copy('C:\CLOSER\Python\\assets\linking.xlsx', self.path() + 'resources')
        else:
            print 'linking.xlsx already copied'
        if not os.path.exists(self.path() + 'mapping.xlsx'):
            shutil.copy('C:\CLOSER\Python\\assets\mapping.xlsx', self.path() + 'resources')
        else:
            print 'mapping.xlsx already copied'

    def copyindexfiles(self):
        if not os.path.exists(self.path() + 'index_files'):
            shutil.copytree('C:\CLOSER\Python\\assets\index_files', self.path() + 'index_files')
        else:
            print 'index_files folder already exists'

#populating qlist in mapping.xlsx (BETA)
    def setupmappingxlsx(self):
        with open(self.path() + 'resources\qlist.txt')as t:
            qlistcsv = csv.reader(t, delimiter='|')
            book = open_workbook(self.path() + 'resources\mapping.xlsx')
            wb = xl_copy.copy(book)
            ws = wb.get_sheet(2)
            for i, row in enumerate(qlistcsv):
                ws.write(i, 0, row[1])
                ws.write(i, 1, row[3])
            wb.save(self.path() + 'resources\mapping_new.xlsx')