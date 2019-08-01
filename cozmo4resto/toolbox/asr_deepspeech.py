# Instructions:


#------------------------
# For GPU version:
# deepspeeh-gpu:
# https://github.com/mozilla/DeepSpeech#cuda-dependency

# Install cudnn version 7.6, and cudatoolkit 10.0
# conda install cudnn=7.6.0 cudatoolkit=10.0
# Then install deepspeech:
# pip install deepspeech-gpu

#------------------------
# For CPU version:
# pip install deepspeech

#------------------------

# Download models:
# wget https://github.com/mozilla/DeepSpeech/releases/download/v0.5.1/deepspeech-0.5.1-models.tar.gz
# tar xvfz deepspeech-0.5.1-models.tar.gz

from __future__ import absolute_import, division, print_function

import argparse
import numpy as np
import shlex
import subprocess
import sys
import wave

from deepspeech import Model, printVersions
from timeit import default_timer as timer

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

# Define the sample rate for audio

SAMPLE_RATE = 16000
# These constants control the beam search decoder

# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
LM_ALPHA = 0.75

# The beta hyperparameter of the CTC decoder. Word insertion bonus.
LM_BETA = 1.85


# These constants are tied to the shape of the graph used (changing them changes
# the geometry of the first layer), so make sure you use the same constants that
# were used during training

# Number of MFCC features to use
N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9


def convert_samplerate(audio_path):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path), SAMPLE_RATE)
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use {}hz files or install it: {}'.format(SAMPLE_RATE, e.strerror))

    return SAMPLE_RATE, np.frombuffer(output, np.int16)


def metadata_to_string(metadata):
    return ''.join(item.character for item in metadata.items)


class VersionAction(argparse.Action):
    def __init__(self, *args, **kwargs):
        super(VersionAction, self).__init__(nargs=0, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        printVersions()
        exit(0)

def load_deepspeech_model(model='deepspeech-0.5.1-models/output_graph.pb', alphabet='deepspeech-0.5.1-models/alphabet.txt', lm='deepspeech-0.5.1-models/lm.binary', trie='models/trie'):
    print('Loading model from file {}'.format(model), file=sys.stderr)
    model_load_start = timer()
    ds = Model(model, N_FEATURES, N_CONTEXT, alphabet, BEAM_WIDTH)
    model_load_end = timer() - model_load_start
    print('Loaded model in {:.3}s.'.format(model_load_end), file=sys.stderr)

    if lm and trie:
        print('Loading language model from files {} {}'.format(lm, trie), file=sys.stderr)
        lm_load_start = timer()
        ds.enableDecoderWithLM(alphabet, lm, trie, LM_ALPHA, LM_BETA)
        lm_load_end = timer() - lm_load_start
        print('Loaded language model in {:.3}s.'.format(lm_load_end), file=sys.stderr)

    return ds

def stt_deepspeech_numpy(y,fs):
    '''

    :param y: a float32 numpy array between 0 and 1 containing audio waveform data
    :param fs: sampling frequency. You should resample your audio to 16000 Hz for better
    performance. Because the model was trained with that
    :return:
    '''
    ds = load_deepspeech_model()

    print('Running inference.', file=sys.stderr)
    inference_start = timer()

    v = (y * 32767).astype(np.int16)
    text = ds.stt(v, fs)

    print(text)
    inference_end = timer() - inference_start
    audio_length=len(y)/fs
    print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)

    return text, inference_end


def stt_deepspeech(audio='/media/adminpc/DATA/databases/IEMOCAP_speech_only/Session1/sentences/wav/Ses01F_impro01/Ses01F_impro01_F004.wav',
                   model='deepspeech-0.5.1-models/output_graph.pb', alphabet='deepspeech-0.5.1-models/alphabet.txt', lm='deepspeech-0.5.1-models/lm.binary', trie='models/trie'):

    ds=load_deepspeech_model(model, alphabet, lm, trie)

    fin = wave.open(audio, 'rb')
    fs = fin.getframerate()
    if fs != SAMPLE_RATE:
        print('Warning: original sample rate ({}) is different than {}hz. Resampling might produce erratic speech recognition.'.format(fs, SAMPLE_RATE), file=sys.stderr)
        fs, audio = convert_samplerate(audio)
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    audio_length = fin.getnframes() * (1/SAMPLE_RATE)
    fin.close()

    print('Running inference.', file=sys.stderr)
    inference_start = timer()
    text=ds.stt(audio, fs)
    print(text)
    inference_end = timer() - inference_start
    print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)


    return text, inference_end


def main():
    parser = argparse.ArgumentParser(description='Running DeepSpeech inference.')
    parser.add_argument('--model', required=True,
                        help='Path to the model (protocol buffer binary file)')
    parser.add_argument('--alphabet', required=True,
                        help='Path to the configuration file specifying the alphabet used by the network')
    parser.add_argument('--lm', nargs='?',
                        help='Path to the language model binary file')
    parser.add_argument('--trie', nargs='?',
                        help='Path to the language model trie file created with native_client/generate_trie')
    parser.add_argument('--audio', required=True,
                        help='Path to the audio file to run (WAV format)')
    parser.add_argument('--version', action=VersionAction,
                        help='Print version and exits')
    parser.add_argument('--extended', required=False, action='store_true',
                        help='Output string from extended metadata')
    args = parser.parse_args()

    print('Loading model from file {}'.format(args.model), file=sys.stderr)
    model_load_start = timer()
    ds = Model(args.model, N_FEATURES, N_CONTEXT, args.alphabet, BEAM_WIDTH)
    model_load_end = timer() - model_load_start
    print('Loaded model in {:.3}s.'.format(model_load_end), file=sys.stderr)

    if args.lm and args.trie:
        print('Loading language model from files {} {}'.format(args.lm, args.trie), file=sys.stderr)
        lm_load_start = timer()
        ds.enableDecoderWithLM(args.alphabet, args.lm, args.trie, LM_ALPHA, LM_BETA)
        lm_load_end = timer() - lm_load_start
        print('Loaded language model in {:.3}s.'.format(lm_load_end), file=sys.stderr)

    fin = wave.open(args.audio, 'rb')
    fs = fin.getframerate()
    if fs != SAMPLE_RATE:
        print('Warning: original sample rate ({}) is different than {}hz. Resampling might produce erratic speech recognition.'.format(fs, SAMPLE_RATE), file=sys.stderr)
        fs, audio = convert_samplerate(args.audio)
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    audio_length = fin.getnframes() * (1/SAMPLE_RATE)
    fin.close()

    print('Running inference.', file=sys.stderr)
    inference_start = timer()
    if args.extended:
        print(metadata_to_string(ds.sttWithMetadata(audio, fs)))
    else:
        print(ds.stt(audio, fs))
    inference_end = timer() - inference_start
    print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)

if __name__ == '__main__':
    #main()
    stt_deepspeech()