import zmq
import json
from abc import ABC, abstractmethod

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
    """using zmq for connecting"""

    def __init__(self, addr_client = None, addr_server = None):
        super(CozmoConnector, self).__init__(addr_client, addr_server)
    
    def run_client(self, data, stop_msg="STOP", address = None):
        """zmq rep req implementation as client"""
        if address is None:
            address = self.addr_client
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.bind(address)
        print('Sending the JSON data')
        socket.send_json(data)
        print('JSON data sent')
        print('Waiting for reception')
        json_data = socket.recv_json()
        print('Data received!')
        print('-----------------------------')
        return json_data

    def run_server(self, func, address = None, stop_msg="STOP", break_json_data=''):
        """zmq rep req implementation as client"""
        if address is None:
            address = self.addr_server
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.connect(address)
        while True:
            print('Waiting for request')
            msg = socket.recv_json()
            if msg['data'] == stop_msg:
                socket.send_json(break_json_data)
                print('Connection stopped')
                break
            print('Processing message received')
            json_data = func(msg)
            print('Sending JSON data')
            socket.send_json(json_data)
            print('Data sent')
            print('-----------------------------')