from Module import *
from Connector import *

def dm(input):
    dct = {'potato':'coconut', 'banana':'papaya', 'stop':'stop'}
    try:
        output = dct[input]
    except:
        output = "Nothing I know!"
    return output

class DMModule(CozmoModule):
    def get_next_state(self):
        if self.jdata['data'] == "stop":
            return 'stop'
        return 'tts'

dm_connector = CozmoConnector(addr_server='127.0.0.1:5001')
dm_module = DMModule(dm)
dm_module.patch_connector(dm_connector)
dm_module.run_server()
