from statemachine import State, StateMachine
import json
import uuid

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

class CozmoBehavior(object):
    def __init__(self, graph, state_dct, json_data = None, stop_condition = False):
        self.graph = graph
        self.state_dct = state_dct
        self.json_data = json_data
        self.stop_condition = stop_condition

    def run_graph(self, json_data = None):
        if json_data is not None:
            self.json_data = json_data
        while True:
            cur_func = self.state_dct[self.graph.current_state]
            json_data, next_state = cur_func.run(json_data)
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