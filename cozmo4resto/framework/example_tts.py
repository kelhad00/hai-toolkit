from gtts import gTTS
from Connector import CozmoConnector
from Module import CozmoModule

def tts(text):
    name = str(uuid.uuid4().int)[:10]
    tts = gTTS(text, 'en')
    tts.save('potato_'+name+'.wav')


class TTSModule(CozmoModule):
    def get_next_state(self):
        return 'dm'

tts_connector = CozmoConnector(addr_server='tcp://127.0.0.1:5002')
tts_module = TTSModule(tts)
tts_module.patch_connector(tts_connector)
tts_module.run_server()
