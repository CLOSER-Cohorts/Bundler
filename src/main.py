__author__ = 'umidqssh'
from application import Application
#from application import Maplink

import os
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
root = os.path.dirname(__file__)
app = Application(args.portnumber, root)
app.run()
