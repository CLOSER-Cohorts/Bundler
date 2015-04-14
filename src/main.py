__author__ = 'umidqssh'
from application import Application
#from application import Maplink

import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument('-A', action='append_const',help='4-digit port number')
#portnumber = parser.parse_args()

arg_parser = argparse.ArgumentParser(
    description='Create Metadata bundles.'
)
arg_parser.add_argument(
    '--port',
    dest='portnumber',
    required=True,
    help='CADDIES port number',
    type=int,
    nargs='*'
)
args = arg_parser.parse_args()
for port in args.portnumber:
    app = Application(port)

    app.setupFolders()
    app.configfiles()
    app.copymanual()
    app.writeddixml()
    app.writeindexhtm()
    app.copyindexfiles()
    #app.setupResources()
    app.writelistfiles()
    app.copyfiles()





#app = Maplink()
#app.setupmappingxlsx()
