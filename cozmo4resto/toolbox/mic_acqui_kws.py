import pyaudio
import numpy as np
import wave
import collections
import soundfile
import time

# This simport is dependent of https://github.com/Picovoice/wakeword-benchmark
# it should be cloned in the same folder of this file with the name "kws"
from use_engine import *
from ringBuffer import RingBuffer

from sys import byteorder
from array import array

"""
window_duration_ms needs to be large enough to contain all the keyword (for KWS)
                         to be large enough to contain all the sentence (for ASR)
frame_duration_ms = (1000.0 / sample_rate)
"""



RATE = 16000
THRESHOLD = 2000
#CHUNK_SIZE = 1024*1
CHUNK_SIZE = int(RATE*0.8)
FORMAT = pyaudio.paInt16
CHANNELS = 6
size = RATE * 3
INDEX = 2


HT = 0 #NEW
BUFFER = [] #NEW
# size = int(window_duration_ms/frame_duration_ms)

from scipy.io.wavfile import write
def save_file(sample_width, data, rate):
    for i in range(len(data)):
        tmp = array('h')
        tmp = data[i].get_data()
        write('test' + str(i) + '.wav',rate,tmp)
        
        #wf = wave.open('test' + str(i) + '.wav', 'wb')
        #wf.setnchannels(1)
        #wf.setsampwidth(sample_width)
        #wf.setframerate(rate)
        #wf.writeframes(tmp)
        #wf.close()
        
def kws_snowboy(data):
#    np.save('array1.npy', data)
    sb=SnowboyEngine('alexa', 1)
    res=sb.process(data)
#    print(res)
    return res

def callback(in_data, frame_count, time_info, flag): #NEW
    global BUFFER#, HT
    for i in range(CHANNELS) :
        snd_data = (array('h', in_data)[i::CHANNELS])
#    if max(snd_data)>THRESHOLD :
        BUFFER[i].add(snd_data)
        
    
#    if HT >= 100 :
#        print('Direction : ')
#        HT = 0
#        return(None, pyaudio.paComplete)
#    else:
    start=time.time()
    spotted=kws_snowboy(BUFFER[0].get_data())
    duration=time.time()-start
    print('kws time:')
    print(duration)
    print(spotted)
    if spotted:
        print('keyword spotted')
            #print('My name is Cozmo !')
#            return(None, pyaudio.paComplete)
    return(None, pyaudio.paContinue)
        
def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.
    """
    global HT, BUFFER
    BUFFER = []
    for i in range(CHANNELS) :
        BUFFER.append(RingBuffer(size))
        
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
        input=True, input_device_index=INDEX,
        frames_per_buffer=CHUNK_SIZE,   stream_callback = callback) #NEW

    print("please speak a word into the microphone")
    
#    HT = 0
#    buffer = []
#    for i in range(CHANNELS) :
#        buffer.append(RingBuffer(size))
    while stream.is_active(): #NEW
#        HT += 1
        time.sleep(0.5) #NEW

    stream.stop_stream() #NEW
    stream.close() #NEW
    
    
#    while 1:   
#        tmp = array('h')
#        read = stream.read(CHUNK_SIZE)#, exception_on_overflow = False)
#        for i in range(CHANNELS) :
#            snd_data = (array('h', read)[i::CHANNELS])
#            if byteorder == 'big':
#                snd_data.byteswap()
#            buffer[i].add(snd_data)
#        HT +=1
#        if HT == 50 :
#            break
#        print(HT)
#        for j in range(buffer[1].len()) :
#            f = buffer[1].get_data(j) 
#            tmp.append(f)
#        tmp = np.array(tmp, dtype = np.int16)
#        if kws(tmp) : break
#    sample_width = p.get_sample_size(FORMAT)
#    stream.stop_stream()
#    stream.close()
#    p.terminate()


    buffer = BUFFER #NEW
    sample_width = p.get_sample_size(FORMAT) #NEW
    
    
    if (CHANNELS)== 6 :
        for i in range(3):
            buffer[i]=buffer[i*2+1]
        buffer = buffer[:3]
    return sample_width, buffer, RATE

if __name__ == '__main__':
    sample_width, audio, rate = record()
    print(len(audio))
    save_file(sample_width, audio, rate)
    print("done - result")
