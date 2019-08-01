import json
from abc import ABC, abstractmethod
from example_functions import dm, asr, tts

class Module(ABC):
    def __init__(self, func):
        self.func = func #function of the module
    
    @abstractmethod
    def call(self, json_data=None):
        """call the function here"""
        pass

    @adbstractmethod
    def patch_connector(self, connector):
        """patch connector to Module"""
        pass

class CozmoModule(Module):
    """implement json inputs and outputs processing.
    
    Can be patched with Connector module
    
    Args:
        Module ([type]): [description]
    
    Raises:
        AttributeError: [description]
        ValueError: [description]
        ValueError: [description]
        ValueError: [description]
    
    Returns:
        [type]: [description]
    """

    def __init__(self, func, json_data=None):
        """input function to be called and initialize json_data.
        
        Args:
            func (callable): If input not JSON, implement json_data pre-processing.
            json_data (JSON or dict, optional): Defaults to None.
        """
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
        jdata = json.loads(self.json_data)
        next_state = self.get_next_state(data) #function does not return anything yet
        jdata['data'] = data
        jdata['next_state'] = next_state
        return jdata

    def get_next_state(self, data):
        '''implement next state logic'''
        pass

    def patch_connector(self, connector):
        setattr(self, 'connector')

    # def add_connector(self, connector):
    #     ### TODO: replace this part with more robust test
    #     # must be adequate with the Connector class
    #     if not hasattr(connector, 'run_server'):
    #         raise AttributeError('connector must be a Connector object')
    #     ###
    #     self.connector = connector

    # def run_connector(self):
    #     if "connector" not in self.__dict__:
    #         raise ValueError("Must add_connector first")
    #     self.connector.run_server()

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