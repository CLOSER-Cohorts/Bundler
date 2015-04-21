__author__ = 'umidqssh'

import os

class Patcher:
    def __init__(self, port):
        dir = os.path.dirname(__file__)
        self.assets = os.path.join(dir,"..\\assets\\")

    def patchindexhtm(self, text):
        with open(self.assets + '\patch.txt', 'r') as f:
            patch = f.read()
            search = '</head>'
            text = text.replace('/stylesheets','index_files').replace('/javascripts','index_files').replace('/images','index_files')
            text = text.replace(search, patch+'\n'+search)
            return text