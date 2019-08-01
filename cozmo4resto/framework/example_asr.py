import speech_recognition as sr
from Connector import CozmoConnector

def asr():
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        audio = rec.record(source, 5)
    text = rec.recognize_google(audio)
    return text


class ASRModule(CozmoModule):
    def get_next_state(self):
        return 'dm'

asr_connector = Connector(addr_server='127.0.0.1:5000')
asr_module = ASRModule(asr)
asr_module.patch_connector(asr_connector)
asr_module.run_server()
