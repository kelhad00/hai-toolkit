import zmq

def get_text():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5000")

    msg = 'launch ASR'
    socket.send(msg)
    text = socket.recv()
    print('User said:{}'.format(text))
    return text