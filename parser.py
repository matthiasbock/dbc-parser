#
# Console application making use of the DBC library
#

from dbc import *
from sys import argv, exit

if len(arv) < 2:
    print "Usage: " + argv[0] + " <filename.dbc>"
    exit()

filename = argv[1]

dbc = DBC()
dbc.load(filename)

print dbc
