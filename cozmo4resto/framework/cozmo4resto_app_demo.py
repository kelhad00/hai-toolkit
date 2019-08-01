from statemachine import State, StateMachine
from Connector import *
from Module import *
from Behavior import *

class CozmoStates(StateMachine):
    """Build graph for Cozmo behavior"""
    asr = State("asr", initial=True)
    dm = State("dm")
    tts = State("tts")
    stop = State("stop")#has no connector

    listen = tts.to(asr)
    think = asr.to(dm)
    speak = dm.to(tts)
    finish = dm.to(stop)

if __name__ == "__main__":
    graph = CozmoStates()
    connector_asr = CozmoConnector(addr_client='tcp://127.0.0.1:5000')
    connector_dm = CozmoConnector(addr_client='tcp://127.0.0.1:5001')
    connector_tts = CozmoConnector(addr_client='tcp://127.0.0.1:5002')
    state_dct = {
        'asr':connector_asr,
        'dm':connector_dm,
        'tts':connector_tts
    }
    
    behav = CozmoBehavior(graph, state_dct)
    behav.run_graph()
    print("Interaction is Done!")