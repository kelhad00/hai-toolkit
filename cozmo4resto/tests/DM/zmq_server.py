import time
import zmq
import sys
from asr import asr

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5000")

while True:
    msg = socket.recv()
    print("Processing %s" % msg, end='')
    if msg == 'launch ASR':
        text = asr()
    socket.send(text)