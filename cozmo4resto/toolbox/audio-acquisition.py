import numpy as np
import pyaudio
import wave
import time
import argparse
import os

FORMAT = pyaudio.paInt16
CHANNELS = 1
INDEX = 1

def get_args():
    desc = "Audio acquisition Command Line Tool"
    epilog = """
    Saves audio into wav files, located in a folder given by the name of the speaker
    """
    parser = argparse.ArgumentParser(description=desc, epilog=epilog,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-n', '--name',
                        help='Person speaking', default='Default',
                        required=False)

    parser.add_argument('-f', '--file',
                        help='Name of the saved wav file', default='test',
                        required=False)

    parser.add_argument('-d', '--duration',
                        help='Duration of the wav file (in seconds)', default=5,
                        type=float, required=False)

    parser.add_argument('-c', '--chunk',
                        help='Chunk size (in seconds)', default=1,
                        type=float, required=False)
    
    parser.add_argument('-r', '--rate',
                        help='Sampling rate', default=16000,
                        choices=[8000, 16000, 24000, 44100, 48000], required=False)

    return parser.parse_args()

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

def save(path, data, width, rate):
    """
    Saves the data recorded in a .wav file
    
    Arguments:
        data {bytes} -- Data that will be saved
        width {int} -- Number of bytes in the format used
        rate {int} -- Sampling rate of the saved file
    """
    for i in range(len(data)):
        wf = wave.open(path + '_' + str(i) + '.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(width)
        wf.setframerate(rate)
        wf.writeframes(data[i])
        wf.close()

if __name__ == '__main__':
    global args
    args = get_args()

    path = "../Users/" + str(args.name)
    if not(os.path.exists(path)):
        try:
            os.makedirs(path)
        except OSError:
            print ("Creation of the directory %s failed" %path)
    path = path + "/" + str(args.file)
    start_time = time.time() #Efficiency estimation by timing
    duration = args.duration; chunk_duration = args.chunk; rate = args.rate
    audio, sample_width = record(duration, chunk_duration, rate)
    final_time = time.time() #Efficiency estimation by timing
    save(path, audio, sample_width, rate)
    print("Done : ", final_time - start_time - duration)