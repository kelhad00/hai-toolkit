import collections

from array import array

import numpy as np

class RingBuffer():

    def __init__(self, size = 4096):
        self._buf = collections.deque(maxlen = size)
    
    def add(self, data):
        self._buf.extend(data)

    def get_data(self):
        tmp = array('h')
        for i in range(len(self._buf)):
            tmp.append(self._buf[i])
        tmp = np.array(tmp, dtype = np.int16)
        return tmp
    
    def popleft(self):
        return self._buf.popleft()
    
    def len(self):
        return len(self._buf)