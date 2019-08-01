import json
from Connector import *
from example_functions import dm

potato = CozmoConnector(addr_client = 'tcp://127.0.0.1:5000')
msg = {'data':'coconut'}
potato.run_client(msg)
msg = {'data':'STOP'}
potato.run_client(msg)