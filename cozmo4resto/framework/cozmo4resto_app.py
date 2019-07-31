from statemachine import State, StateMachine
import json
import uuid
import zmq
from abc import ABC, abstractmethod


#TODO: Build test functions to input in CozmoModule class
#TODO: CozmoConnector->CozmoModule to add send and recv with zmq + function using them

class CozmoStates(StateMachine):
    """build graph for cozmo"""
    wondering = State("wonder", initial=True)
    listener = State("listener")
    speaker = State("speaker")

    start_listening = wondering.to(listener)
    speak = listener.to(speaker)
    stop_speaking = speaker.to(wondering)
    listen = speaker.to(listener)
    stop_listening = listener.to(wondering)

class Connector(ABC):
    def __init__(self, add_client, add_server):
        self.add_client = add_client
        self.add_server = add_server
    
    @abstractmethod
    def client(self):
        pass
    
    @abstractmethod
    def server(self):
        pass

class CozmoConnector(Connector):
    '''using zmq for connecting'''

    def __init__(self, add_client = None, add_server = None):
        super(CozmoConnector, self).__init__(add_client, add_server)
    
    def client(self, data, address=None, stop_msg="STOP"):
        if address is not None:
            self.address = address
        print(self.address) #TODO: replace with sending msg with zmq
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(self.address)
        data = json.dumps(data)
        socket.send(data)
        json_data = socket.recv_json()
        return json_data

    def server(self, func, address = None, stop_msg="STOP"):
        if address is not None:
            self.address = address
        print(self.address) #TODO:replace with receiving msg with zmq

        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(self.address)
        while True:
            msg = socket.recv()
            if msg == stop_msg:
                break
            json_data = func(msg)
            socket.send(json_data)

class Module(ABC):
    def __init__(self, func):
        self.func = func #function of the module
    
    @abstractmethod
    def call(self, json_data=None):
        """call the function here"""
        pass

class CozmoModule(Module):
    """Implements inputs and outputs only.
    connections is taken care of by Connector class."""

    def __init__(self, func, next_state, json_data=None):
        super(CozmoModule, self).__init__(func)
        self.next_state = next_state #TODO: improve next_state decision code
        if json_data is None:
            self.json_data = json.dumps({'data':None, 'current_state':None, 'next_state':None})
        else:
            self.json_data = json_data

    def call(self, json_data):
        self.json_data = json_data
        jdata = json.loads(self.json_data)
        data = self.func(jdata['data']) #call function
        next_state = self.get_next_state(data) #function does not return anything yet
        jdata['data'] = data
        jdata['next_state'] = next_state
        return jdata

    def get_next_state(self, data):
        '''implement next state logic'''
        pass #TODO: base decision on list of possible states passed to the class?

    @property
    def json_data(self):
        return self._json_data
    
    @json_data.setter
    def json_data(self, jdata):
        json_must_have = ['data', 'current_state', 'next_state']
        try:
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
        self.json_data = json_data

    def run_graph(self, json_data = None):
        if json_data is not None:
            self.json_data = json_data
        while True:
            func = self.state_dct[self.graph.current_state]
            ### TEMPO
            if isinstance(func, Connector):
                next_state, json_data = func.connect()
            elif isinstance(func, Module):
                json_data, next_state = func.call(json_data)
            ### ###
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
    state_dct = {
        'wonder':[],#can be either a connector or a Module: connector connects to Module; Module is run
        'listener':[],
        'speaker':[]
    }
    behav = CozmoBehavior(graph, state_dct)
    behav.run_graph()
    print("Interaction is Done!")