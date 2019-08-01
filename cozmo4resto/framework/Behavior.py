from abc import ABC, abstractmethod
from statemachine import State, StateMachine

class CozmoBehavior:
    def __init__(self, graph, state_dct, jdata = None):
        self.graph = graph
        self.state_dct = state_dct
        if jdata is None:
            self.jdata = {'data':None, 'current_state':None, 'next_state':None}
        else:
            self.jdata = jdata #info about next state and input data for next state

    def run_graph(self, jdata = None):
        if jdata is None:
            jdata = self.jdata #TODO: add @property for jdata
        while True:
            print("Now in state:{}".format(self.graph.current_state.name))
            func = self.state_dct[self.graph.current_state.name]
            jdata = func.run_client(jdata) #For now all func are connectors
            if self.stop_condition(jdata['next_state']):
                break
            self.update_state(jdata['next_state'])
    
    def update_state(self, next_state):
            if next_state != self.graph.current_state:
                for stt in self.graph.transitions:
                    if (stt.source.name == self.graph.current_state) and (stt.destinations[0].name  == next_state):
                        # if len(stt.destinations)>1:
                        #     raise ValueError("No more than one destination per state.")
                        self.graph.run(stt.destinations[0].identifier)#run transition with string

    def stop_condition(self, next_state):
        if next_state == "stop":
            return True

    @property
    def graph(self):
        return self._graph
    
    @graph.setter
    def graph(self, input_graph):
        if not isinstance(input_graph, StateMachine):
            raise ValueError('Should be an instance of StateMachine class.')
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