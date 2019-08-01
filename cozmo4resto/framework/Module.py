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

    @abstractmethod
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

    def __init__(self, func, jdata=None):
        """input function to be called and initialize json_data.
        
        Args:
            func (callable): If input not JSON, implement json_data pre-processing.
            json_data (JSON or dict, optional): Defaults to None.
        """
        super(CozmoModule, self).__init__(func)
        self.next_state = None
        if jdata is None:
            self.jdata = json.dumps({'data':None, 'current_state':None, 'next_state':None})
        else:
            self.jdata = jdata

    def call(self, jdata):
        self.jdata = jdata
        data = self.func(jdata['data']) #call function
        jdata = self.create_json(data)
        return jdata

    def create_json(self, data):
        next_state = self.get_next_state() #function does not return anything yet
        self.jdata['data'] = data
        self.jdata['next_state'] = next_state
        return jdata

    def get_next_state(self):
        '''implement next state logic'''
        pass

    def patch_connector(self, connector):
        #TODO: test connector
        setattr(self, '_connector', connector) #patch connector to class
        
        def run_client(self, jdata): #define Module method to run client from connector
            self._connector.run_client(jdata)
            
        def run_server(self): #define Module method to run server from connector
            self._connector.run_server(self.call)

        setattr(self, 'run_client', run_client) #create run_client method in Module
        setattr(self, 'run_server', run_server) #create run_server method in Module

    @property
    def jdata(self):
        return self._jdata
    
    @json_data.setter
    def jdata(self, jdata):
        json_must_have = ['data', 'current_state', 'next_state']
        try: #check if jdata is json format
            data = json.loads(jdata)
            for val in json_must_have:
                if val not in data:
                    raise ValueError('JSON input must have: {}'.format(json_must_have))
        except:
            raise ValueError('Input must be JSON and must have {}'.format(json_must_have))
        self._jdata = jdata