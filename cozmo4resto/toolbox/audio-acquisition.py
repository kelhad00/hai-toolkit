import numpy as np
import pyaudio
import wave
import time

g_DURATION = 5 #Seconds
g_CHUNK_DURATION = 1 #Seconds

FORMAT = pyaudio.paInt16
g_RATE = 16000
CHANNELS = 1
INDEX = 1
  
def record(duration, chunk_duration, rate):
    """
    Records audio using microphone
    
    Arguments:
        duration {float} -- Total duration of the recording
        chunk_duration {float} -- Duration of each frame
        rate {int} -- Sampling rate of the microphone
    
    Returns:
        list{bytes}, int -- buffer is the data recorded, sample_width corresponds to the number of bytes in the format used
    """
    buffer = []
    count = 0
    chunk_size = int(chunk_duration*rate)
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=rate,
        input=True, input_device_index=INDEX,
        frames_per_buffer=chunk_size)

    print("Say a something to the microphone : ")
    while count < duration :
        audio_data = stream.read(chunk_size)
        buffer.append(audio_data)
        count += chunk_duration

    stream.stop_stream()
    stream.close()

    sample_width = p.get_sample_size(FORMAT)
    return buffer, sample_width

def save(data, width, rate):
    """
    Saves the data recorded in a .wav file
    
    Arguments:
        data {bytes} -- Data that will be saved
        width {int} -- Number of bytes in the format used
        rate {int} -- Sampling rate of the saved file
    """
    for i in range(len(data)):
        wf = wave.open('test_' + str(i) + '.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(width)
        wf.setframerate(rate)
        wf.writeframes(data[i])
        wf.close()

if __name__ == '__main__':
    tmp = time.time() #Efficiency estimation by timing
    duration = g_DURATION; chunk_duration = g_CHUNK_DURATION; rate = g_RATE
    audio, sample_width = record(duration, chunk_duration, rate)
    fin = time.time() #Efficiency estimation by timing
    save(audio, sample_width, rate)
    print("Done : ", fin - tmp - duration)