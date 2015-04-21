__author__ = 'umidqssh'


import urllib2
import bs4
import os
import shutil
from xlrd import open_workbook
from xlwt import Workbook
from xlutils import copy as xl_copy
import xlsxwriter as xl
import csv


class Application:
    def __init__(self, port):
        self.port = port
        self.prefix = None
        dir = os.path.dirname(__file__)
        self.output = os.path.join(dir, "..\\output\\")
        self.assets = os.path.join(dir,"..\\assets\\")

    def url(self):
        return "http://192.168.52.61:" + str(self.port)

    def scrapePrefix(self):
        if self.prefix == None:
            response = urllib2.urlopen(self.url())
            soup = bs4.BeautifulSoup(response.read())
            div = soup.find(id="version")
            self.prefix = div.h3.string.split(':')[1].lstrip()

    def path(self):
        self.scrapePrefix()
        return self.output + self.prefix + "\\"

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

    #def setupResources(self):
        #if not os.path.exists(self.path() + 'resources'):
            #os.makedirs(self.path() + 'resources')
        #else:
            #print 'Resources folder already created for' + self.prefix

#creating config files
    def configfiles(self):
        files = ['dv.txt','labels.txt','linking.txt','mapping.txt','notes.txt','redactions.txt']
        for i in files:
            if not os.path.exists(self.path() + i):
                file = open(self.path() + i, 'w')
            else:
                print i + ' ' + 'already created'

#getfiles
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
            shutil.copy(self.assets + 'Metadata Delivery Bundle.pdf', self.path())
        else:
             print 'manual already copied'

    def copyfiles(self):
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
            wb.save(self.path() + 'resources\mapping_new.xls')

    def embed_qlist_into_mapping(self):
        with open(self.path() + 'resources\qlist.txt')as t:
            qlistcsv = csv.reader(t, delimiter='|')
            wb = xl.Workbook(self.path() + 'resources\mapping_new.xlsx')
            bold = wb.add_format({'bold': True})
            ws_mtxt = wb.add_worksheet('mapping.txt')
            ws_mtxt.set_tab_color('green')
            ws_mtxt.write(0,0,'=IF(AND(ISBLANK(mapping!D2),ISBLANK(mapping!E2)),mapping!C2,mapping!C2&"$"&IF(ISBLANK(mapping!D2),"0",mapping!D2)&";"&IF(ISBLANK(mapping!E2),"0",mapping!E2))')
            ws_mtxt.write(0,1,'=mapping!A2')
            ws_dvtxt = wb.add_worksheet('dv.txt')
            ws_dvtxt.set_tab_color('green')
            ws_dvtxt.write(0,0,"='DV mapping'!A2")
            ws_dvtxt.write(0,1,'=IF(ISBLANK(\'DV mapping\'!C2),IF(AND(OR(ISBLANK(\'DV mapping\'!F2),ISNA(\'DV mapping\'!F2)),OR(ISBLANK(\'DV mapping\'!G2),ISNA(\'DV mapping\'!G2))),IF(ISNA(\'DV mapping\'!E2),0,\'DV mapping\'!E2),IF(AND(\'DV mapping\'!F2<1,\'DV mapping\'!G2<1),\'DV mapping\'!E2,\'DV mapping\'!E2&"$"&\'DV mapping\'!F2&";"&\'DV mapping\'!G2)),\'DV mapping\'!C2)')
            ws_qlist = wb.add_worksheet('qlist')
            ws_qlist.set_tab_color('blue')
            ws_qlist.write(0,0,'ID',bold)
            ws_qlist.write(0,1,'Question Literal',bold)

            for i, row in enumerate(qlistcsv):
                ws_qlist.write(i+1, 0, row[1])
                ws_qlist.write(i+1, 1, row[3])

            ws_var = wb.add_worksheet('variables')
            ws_var.set_tab_color('blue')
            ws_var.write(0,0,'Variable',bold)
            ws_var.write(0,1,'Label',bold)
            ws_map = wb.add_worksheet('mapping')
            ws_map.set_tab_color('red')
            ws_map.write(0,0,'Variable',bold)
            ws_map.write(0,1,'Label',bold)
            ws_map.write(0,2,'ID',bold)
            ws_map.write(0,3,'X',bold)
            ws_map.write(0,4,'Y',bold)
            ws_map.write(0,5,'Question Literal',bold)
            ws_dv = wb.add_worksheet('DV mapping')
            ws_dv.set_tab_color('red')
            ws_dv.write(0,0,'Derived Variable',bold)
            ws_dv.write(0,1,'Label',bold)
            ws_dv.write(0,2,'Variable',bold)
            ws_dv.write(0,3,'Label',bold)
            ws_dv.write(0,4,'Question',bold)
            ws_dv.write(0,5,'X',bold)
            ws_dv.write(0,6,'Y',bold)
            ws_dv.write(0,7,'Literal',bold)

        wb.close()


    #def setupmappingxlsx(self):
        #with open(self.path() + 'resources\qlist.txt')as t:
            #qlistcsv = csv.reader(t, delimiter='|')
            #book = openpyxl.load_workbook(self.path() + 'resources\mapping.xlsx')
            #sheet = book.get_sheet_names()
            #ws = book.get_sheet_by_name('qlist')
            #for i, row in enumerate(qlistcsv):
                #cell_tmp1 = ws.cell(i, 0)
                #cell_tmp1.value = row[1]
                #cell_tmp2 = ws.cell(i, 1)
                #cell_tmp2.value = row[3]
            #book.save(self.path() + 'resources\mapping_new.xlsx')

    #def setupmappingxlsx(self):
        #with open(self.path() + 'resources\qlist.txt')as t:
            #qlistcsv = csv.reader(t, delimiter='|')
           # book = openpyxl.load_workbook(self.path() + 'resources\mapping.xlsx')
            #sheet = book.get_sheet_names()
            #ws = book.get_sheet_by_name(sheet[2])
            #for i, row in enumerate(qlistcsv):
               # ws.write(i, 0, row[1])
                #ws.write(i, 1, row[3])
            #book.save(self.path() + 'resources\mapping1.xlsx')



                #ws.write(i, 0, row[1])
                #ws.write(i, 1, row[3])
                #print row[1], row[3]