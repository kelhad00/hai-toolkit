import time
import zmq
import sys
import json
from asr import asr

context = zmq.Context()
socket = context.socket(zmq.REP)
print('waiting for message1...')
socket.bind("tcp://127.0.0.1:5555")

while True:
    print('waiting for message2...')
    msg = socket.recv()
    print("Processing %s" % msg, end='')
    text = asr()
    jdata = json.dumps({'data':text})
    socket.send_string(jdata)