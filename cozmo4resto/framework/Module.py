import json
from abc import ABC, abstractmethod

class Module(ABC):
    def __init__(self, func):
        self.func = func #function of the module
    
    @abstractmethod
    def call(self, jdata=None):
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
        """input function to be called and initialize jdata.
        
        Args:
            func (callable): If input not JSON, implement jdata pre-processing.
            jdata (JSON or dict, optional): Defaults to None.
        """
        super(CozmoModule, self).__init__(func)
        self.next_state = None
        if jdata is None:
            self.jdata = {'data':None, 'current_state':None, 'next_state':None}
        else:
            self.jdata = jdata

    def call(self, jdata):
        self.jdata = jdata
        data = self.func(self.jdata['data']) #call function
        jdata = self.create_json(data)
        return jdata

    def create_json(self, data):
        next_state = self.get_next_state() #function does not return anything yet
        self.jdata['data'] = data
        self.jdata['next_state'] = next_state
        return self.jdata

    def get_next_state(self):
        '''implement next state logic'''
        pass

    def patch_connector(self, connector):
        #TODO: test connector
        setattr(self, '_connector', connector) #patch connector to class
        
        def run_client(jdata): #define Module method to run client from connector
            jdata = self._connector.run_client(jdata)#returns data only
            print(jdata)
            return jdata
            
        def run_server(): #define Module method to run server from connector
            self._connector.run_server(self.call)

        setattr(self, 'run_client', run_client) #create run_client method in Module
        setattr(self, 'run_server', run_server) #create run_server method in Module

    @property
    def jdata(self):
        return self._jdata
    
    @jdata.setter
    def jdata(self, jdata):
        json_must_have = ['data', 'current_state', 'next_state']
        try: #check if jdata is json format
            for val in json_must_have:
                if val not in jdata:
                    raise ValueError('JSON input must have: {}'.format(json_must_have))
        except:
            raise ValueError('Input must be JSON and must have {}'.format(json_must_have))
        self._jdata = jdata