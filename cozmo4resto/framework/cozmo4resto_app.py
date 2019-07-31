from statemachine import State, StateMachine
import json
import uuid
import zmq
from abc import ABC, abstractmethod


#TODO: Build test functions to input in CozmoModule class
#TODO: CozmoConnector->CozmoModule to add send and recv with zmq + function using them

#EXAMPLE FUNCTIONS
import speech_recognition as sr
def asr():
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        audio = rec.record(source, 5)
    text = rec.recognize_google(audio)
    return text

from gtts import gTTS
def gtts(text):
    name = str(uuid.uuid4().int)[:10]
    tts = gTTS(text, 'en')
    tts.save('potato_'+name+'.wav')

def dm(input):
    dct = {'potato':'coconut', 'banana':'papaya'}
    try:
        output = dct[input]
    except:
        output = "Nothing I know!"
    return output
    
# class CozmoStates(StateMachine):
#     """build graph for cozmo"""
#     wandering = State("wander", initial=True)
#     listener = State("listener")
#     speaker = State("speaker")

#     start_listening = wandering.to(listener)
#     speak = listener.to(speaker)
#     stop_speaking = speaker.to(wandering)
#     listen = speaker.to(listener)
#     stop_listening = listener.to(wandering)

class CozmoStates(StateMachine):
    """Build graph for Cozmo behavior"""
    asr = State("asr", initial=True)
    dm = State("dm")
    tts = State("tts")

    listen = tts.to(asr)
    think = asr.to(dm)
    speak = dm.to(tts)

class Connector(ABC):
    def __init__(self, addr_client, addr_server):
        self.addr_client = addr_client
        self.addr_server = addr_server
    
    @abstractmethod
    def run_client(self):
        pass
    
    @abstractmethod
    def run_server(self):
        pass

class CozmoConnector(Connector):
    '''using zmq for connecting'''

    def __init__(self, addr_client = None, addr_server = None):
        super(CozmoConnector, self).__init__(addr_client, addr_server)
    
    def run_client(self, data, stop_msg="STOP"):
        '''zmq rep req implementation'''
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.bind(self.address)
        data = json.dumps(data)
        socket.send_json(data)
        json_data = socket.recv_json()
        return json_data

    def run_server(self, func, address = None, stop_msg="STOP"):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.connect(self.address)
        while True:
            msg = socket.recv_json()
            if msg == stop_msg:
                break
            json_data = func(msg)
            socket.send_json(json_data)

class Module(ABC):
    def __init__(self, func):
        self.func = func #function of the module
    
    @abstractmethod
    def call(self, json_data=None):
        """call the function here"""
        pass

    @abstractmethod
    def add_connector(self, connector):
        """connector is instance of Connector"""
        pass

    @abstractmethod
    def run_connector(self):
        """must add_connector before"""
        pass


class CozmoModule(Module):
    """Implements inputs and outputs only.
    connections is taken care of by Connector class."""

    def __init__(self, func, json_data=None):
        super(CozmoModule, self).__init__(func)
        self.next_state = None
        if json_data is None:
            self.json_data = json.dumps({'data':None, 'current_state':None, 'next_state':None})
        else:
            self.json_data = json_data

    def call(self, json_data):
        self.json_data = json_data
        jdata = json.loads(self.json_data)
        data = self.func(jdata['data']) #call function
        jdata = self.create_json(data)
        return jdata

    def create_json(self, data):
        next_state = self.get_next_state(data) #function does not return anything yet
        jdata['data'] = data
        jdata['next_state'] = next_state
        return jdata

    def get_next_state(self, data):
        '''implement next state logic'''
        pass #TODO: base decision on list of possible states passed to the class?

    def add_connector(self, connector):
        ### TODO: replace this part with more robust test
        if not hasattr(connector, 'run_server'):
            raise AttributeError('connector must be a Connector object')
        ###
        self.connector = connector

    def run_connector(self):
        if "connector" not in self.__dict__:
            raise ValueError("Must add_connector first")
        self.connector.run_server()

    @property
    def json_data(self):
        return self._json_data
    
    @json_data.setter
    def json_data(self, jdata):
        json_must_have = ['data', 'current_state', 'next_state']
        try: #check if jdata is json format
            data = json.loads(jdata)
            for val in json_must_have:
                if val not in data:
                    raise ValueError('JSON input must have: {}'.format(json_must_have))
        except:
            raise ValueError('Input must be JSON and must have {}'.format(json_must_have))
        self._json_data = jdata

class CozmoBehavior:
    def __init__(self, graph, state_dct, json_data = None):
        self.graph = graph
        self.state_dct = state_dct
        self.json_data = json_data#info about next state and input data for next state

    def run_graph(self, json_data = None):
        if json_data is not None:
            self.json_data = json_data
        while True:
            func = self.state_dct[self.graph.current_state]
            func.run_client(json_data)#For now all func are connectors
            if self.stop_condition(next_state):
                break
            self.update_state(next_state)
    
    def update_state(self, next_state):
            if next_state != self.graph.current_state:
                for stt in self.graph.transitions:
                    if stt.source.name == self.graph.current_state:
                        # if len(stt.destinations)>1:
                        #     raise ValueError("No more than one destination per state.")
                        self.graph.run(stt.destinations.identifier)#run transition with string

    def stop_condition(self, next_state):
        if next_state == "end":
            return True

    @property
    def graph(self):
        return self._graph
    
    @graph.setter
    def graph(self, input_graph):
        if not isinstance(input_graph, CozmoStates):
            raise ValueError('Should be an instance of CozmoStates class.')
        else:
            self._graph = input_graph

    @property
    def state_dct(self):
        return self._state_dct
    
    @state_dct.setter
    def state_dct(self, dct):
        if not isinstance(dct, dict):
            raise ValueError('Should be a dict.')
        else:
            self._state_dct = dct


if __name__ == "__main__":
    graph = CozmoStates()
    connector_asr = CozmoConnector(add_client='127.0.0.1:5000', add_server='127.0.0.1:5000')
    connector_dm = CozmoConnector(add_client='127.0.0.1:5001', add_server='127.0.0.1:5001')
    connector_tts = CozmoConnector(add_client='127.0.0.1:5002', add_server='127.0.0.1:5002')
    state_dct = {
        'asr':connector_asr,
        'dm':connector_dm,
        'tts':connector_tts
    }
    behav = CozmoBehavior(graph, state_dct)
    behav.run_graph()
    print("Interaction is Done!")