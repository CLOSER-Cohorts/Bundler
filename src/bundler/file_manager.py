__author__ = 'umidqssh'

import shutil
import os
from patcher import Patcher
from scraper import Scraper


class FileManager:
    def __init__(self, port):
        self.prefix = None
        self.port = port
        dir = os.path.dirname(__file__)
        self.output = os.path.join(dir, "..\\output\\")
        self.assets = os.path.join(dir,"..\\assets\\")
#output directory
    def path(self):
        Scraper.scrapePrefix()
        return self.output + self.prefix + "\\"
#creates bundle folder and resources folder within bundle folder
    def setupFolders(self):
        if not os.path.exists(self.output + self.prefix):
            os.makedirs(self.output + self.prefix)
        else:
            print 'Bundle folder already created for' + ' ' + self.prefix
        if not os.path.exists(self.path() + 'resources'):
            os.makedirs(self.path() + 'resources')
        else:
            print 'Resources folder already created for' + ' ' + self.prefix

#creating txt files in resources folder
    def write_Qlist(self):
        text = Scraper.getQlist()
        if not os.path.isfile(self.path() + 'resources\qlist.txt'):
            with open(self.path() + 'resources\qlist.txt', 'w') as f:
                f.write(text)
        else:
            print 'qlist.txt already downloaded'

    def write_Slist(self):
        text2 = Scraper.getSlist()
        if not os.path.isfile(self.path() + 'resources\slist.txt'):
            with open(self.path() + 'resources\slist.txt', 'w') as f:
                f.write(text2)
        else:
            print 'slist.txt already downloaded'

#creating index.htm
    def writeindexhtm(self):
        text = Scraper.getIndexhtm()
        if not os.path.isfile(self.path() + 'index.htm'):
            with open(self.path() + 'index.htm', 'w') as f:
                f.write(Patcher.patchindexhtm(text))
        else:
            print 'index.htm already saved'

#creating ddi.xml
    def writeddixml(self):
        text = Scraper.getddixml()
        if not os.path.isfile(self.path() + 'ddi.xml'):
            with open(self.path() + 'ddi.xml', 'w') as f:
                f.write(text)
        else:
            print 'ddi.xml already saved'

#copying files from TOOLS
    def copymanual(self):
        self.path()
        if not os.path.exists(self.path() + 'Metadata Delivery Bundle.pdf'):
            shutil.copy(self.assets + 'Metadata Delivery Bundle.pdf', self.path())
        else:
             print 'manual already copied'

    def copyTOOLSfiles(self):
        self.path()
        if not os.path.exists(self.path() + 'CV.txt'):
            shutil.copy(self.assets + 'CV.txt', self.path() + 'resources')
        else:
            print 'CV.txt already copied'
        if not os.path.exists(self.path() + 'linking.xlsx'):
            shutil.copy(self.assets + 'linking.xlsx', self.path() + 'resources')
        else:
            print 'linking.xlsx already copied'
        if not os.path.exists(self.path() + 'mapping.xlsx'):
            shutil.copy(self.assets + 'mapping.xlsx', self.path() + 'resources')
        else:
            print 'mapping.xlsx already copied'

    def copyindexfiles(self):
        if not os.path.exists(self.path() + 'index_files'):
            shutil.copytree(self.assets + 'index_files', self.path() + 'index_files')
        else:
            print 'index_files folder already exists'