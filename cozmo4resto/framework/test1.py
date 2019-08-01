from Connector import *
from example_functions import dm

potato = CozmoConnector(addr_server = 'tcp://127.0.0.1:5000')
potato.run_server(dm)