from statemachine import State, StateMachine
import json
import uuid
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
    def __init__(self, address):
        self.address = address
    
    @abstractmethod
    def send_msg(self):
        pass
    
    @abstractmethod
    def recv_msg(self):
        pass

class CozmoConnector(Connector):
    def __init__(self, address):
        super(CozmoConnector, self).__init__(address)
    
    def send_msg(self, data, to_address=None):
        if to_address is not None:
            self.address = to_address
        print(self.address) #TODO: replace with sending msg with zmq
    
    def recv_msg(self, from_address = None):
        if from_address is not None:
            self.address = from_address
        self.address = from_address
        print(self.address) #TODO:replace with receiving msg with zmq

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

    def __init__(self, func, next_state):
        super(CozmoModule, self).__init__(func)
        self.connected = False
        self.next_state = next_state #TODO: improve next_state decision code

    
    def call(self, json_data=None):
        if not self.connected:
            json_data = self.func(json_data)
            next_state = self.next_state #TODO: improve next_state decision code
        else:
            json_data = self.func(json_data)
            next_state = self.next_state #TODO: improve next_state decision code

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, connect):
        if isinstance(connect, bool):
            self._connected = connect
        else:
            raise AttributeError("connected must be of the type bool")

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