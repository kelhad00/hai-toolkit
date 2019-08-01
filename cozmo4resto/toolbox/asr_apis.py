# IBM speech to text in python
# source: https://cloud.ibm.com/apidocs/speech-to-text?code=python
import time
# after creating a stt resource, go to https://cloud.ibm.com/resources
# get the API key and write it here:

apikey='xxxxx'

def stt_ibm(path='/media/adminpc/DATA/databases/IEMOCAP_speech_only/Session1/sentences/wav/Ses01F_impro01/Ses01F_impro01_F004.wav',
            url='https://gateway-lon.watsonplatform.net/speech-to-text/api'):
    from ibm_watson import SpeechToTextV1
    import json


    speech_to_text = SpeechToTextV1(
        iam_apikey=apikey,
        url=url
    )

    # speech_models = speech_to_text.list_models().get_result()
    # print(json.dumps(speech_models, indent=2))

    start=time.time()
    with open(path,'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/wav',
        ).get_result()
    # print(json.dumps(speech_recognition_results, indent=2))
    duration=time.time()-start
    try:
        text=speech_recognition_results['results'][0]['alternatives'][0]['transcript']
    except:
        text=''
        duration=0
    print(text)
    print(duration)
    return text, duration


import struct
def array_to_bytes(y):
    '''

    :param y: a float numpy array between 0 and 1 containing audio waveform data
    :return: bytes coresponding to PCM WAV format
    '''
    bytes = ''.encode()
    for i in range(len(y)):
        value = int(32767.0 * y[i])
        data = struct.pack('<h', value)
        bytes += data

    return bytes

def numpy_to_AudioData(y,fs,n_bytes=2):
    import speech_recognition as sr
    '''
    :param y: a float numpy array between 0 and 1 containing audio waveform data
    :param fs: a float sampling frequency
    :param n_bytes: number of bytes per sample ( 2 for standard wav files)
    :return: 
    '''
    bytes=array_to_bytes(y)
    audio = sr.AudioData(bytes, fs, n_bytes)
    return audio

def numpy_to_file_object(y,fs):
    import io
    audio=numpy_to_AudioData(y,fs)
    wav_bytes=audio.get_wav_data()

    f = io.BytesIO(wav_bytes)

    return f



# source:
# https://pypi.org/project/SpeechRecognition/
# for pyaudio: sudo apt-get install portaudio19-dev python-all-dev python3-all-dev && pip install pyaudio
# for pocket sphinx:
# see https://github.com/bambocher/pocketsphinx-python
# I needed to do: sudo apt-get install libpulse-dev

def stt_google_AudioData(audio):
    import speech_recognition as sr
    r = sr.Recognizer()
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`

        start = time.time()
        text=r.recognize_google(audio)
        duration = time.time() - start
        print("Google Speech Recognition thinks you said :" + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        text = ''
        duration=0
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        text = ''
        duration = 0

    return text, duration

def stt_google_numpy(y,fs):
    audio=numpy_to_AudioData(y,fs)
    return stt_google_AudioData(audio)

def stt_google_path(AUDIO_FILE = '/media/adminpc/DATA/databases/IEMOCAP_speech_only/Session1/sentences/wav/Ses01F_impro01/Ses01F_impro01_F004.wav'):
    import speech_recognition as sr

    # obtain audio from the microphone
    # r = sr.Recognizer()
    # with sr.Microphone() as source:
    #     print("Say something!")
    #     audio = r.listen(source)

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    return stt_google_AudioData(audio)


# If you want to use this one with a numpy array, you have to use the same as for stt_google_numpy.
def stt_sphinx(AUDIO_FILE = '/media/adminpc/DATA/databases/IEMOCAP_speech_only/Session1/sentences/wav/Ses01F_impro01/Ses01F_impro01_F004.wav'):
    import speech_recognition as sr

    # obtain audio from the microphone
    # r = sr.Recognizer()
    # with sr.Microphone() as source:
    #     print("Say something!")
    #     audio = r.listen(source)

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Sphinx
    try:
        start=time.time()
        text=r.recognize_sphinx(audio)
        duration=time.time()-start
        print("Sphinx thinks you said :" + text)
        print(duration)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        text=''
        duration=0
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
        text = ''
        duration = 0

    return text, duration





####### The following functions come from: #########
# https://github.com/sterling239/audio-emotion-recognition
import os
import numpy as np
import pandas as pd
def get_all_files(path_to_wav):
    files = os.listdir(path_to_wav)
    return files


def get_emotions(path_to_emotions, filename):
    # type: (object, object) -> object
    f = open(path_to_emotions + filename, 'r').read()
    # print f
    # print f.split('\n')
    f = np.array(f.split('\n'))  # np.append(np.array(['']), np.array(f.split('\n')))
    c = 0
    idx = f == ''
    idx_n = np.arange(len(f))[idx]
    emotion = []
    for i in range(len(idx_n) - 2):
        g = f[idx_n[i] + 1:idx_n[i + 1]]
        head = g[0]
        i0 = head.find(' - ')
        start_time = float(head[head.find('[') + 1:head.find(' - ')])
        end_time = float(head[head.find(' - ') + 3:head.find(']')])
        actor_id = head[
                   head.find(filename[:-4]) + len(filename[:-4]) + 1:head.find(filename[:-4]) + len(filename[:-4]) + 5]
        emo = head[head.find('\t[') - 3:head.find('\t[')]
        vad = head[head.find('\t[') + 1:]

        v = float(vad[1:7])
        a = float(vad[9:15])
        d = float(vad[17:23])

        emotion.append({#'start': start_time,
                        #'end': end_time,
                        'id': filename[:-4] + '_' + actor_id,
                        'v': v,
                        'a': a,
                        'd': d,
                        'emotion': emo})
    return emotion

# available_emotions = ['ang', 'exc', 'fru', 'neu', 'sad']

def get_transcriptions(path_to_transcriptions, filename):
    f = open(path_to_transcriptions + filename, 'r').read()
    f = np.array(f.split('\n'))
    transcription = {}

    for i in range(len(f) - 1):
        g = f[i]
        i1 = g.find(': ')
        i0 = g.find(' [')
        ind_id = g[:i0]
        ind_ts = g[i1 + 2:]
        transcription[ind_id] = ind_ts
    return transcription

import re
def load_iemocap(path_to_IEMOCAP='/media/adminpc/DATA/databases/IEMOCAP_speech_only/'):
    data = []
    sessions = ['Session1', 'Session2', 'Session3', 'Session4', 'Session5']
    for session in sessions:
        print(session)
        path_to_wav = os.path.join(path_to_IEMOCAP, session+ '/dialog/wav/')
        path_to_sentences = os.path.join(path_to_IEMOCAP, session+ '/sentences/wav/')
        path_to_emotions = os.path.join(path_to_IEMOCAP, session+ '/dialog/EmoEvaluation/')
        path_to_transcriptions = os.path.join(path_to_IEMOCAP, session+ '/dialog/transcriptions/')

        # files lists dialogs
        files = get_all_files(path_to_wav)
        files = np.array([x for x in files if not x.startswith('.')]) #remove files beginning by '.'
        files=files[[f[-4:] == '.wav' for f in files]]# keep only if ends by '.wav'
        files = [f[:-4] for f in files] # remove this .wav extension from the names
        print(len(files))
        print(files)

        for f in files:
            # f corresponds to one dialog
            emotions = get_emotions(path_to_emotions, f + '.txt')
            transcriptions = get_transcriptions(path_to_transcriptions, f + '.txt')
            for ie, e in enumerate(emotions):
                # It means that we discard files without a category assigned to it...
                # I'm not sure but I suppose it is when the opinions of annotators were not consistent
                # if not(e['emotion']=='xxx'):
                # e['left'] = sample[ie]['left']
                # e['right'] = sample[ie]['right']
                e['database']='IEMOCAP'
                # if '[' in transcriptions[e['id']]:
                #     import pdb;pdb.set_trace()

                transcription=re.sub(' [[A-Z]*] ', '', transcriptions[e['id']])
                transcription=re.sub('[[A-Z]*] ', '', transcription)
                transcription=re.sub(' [[A-Z]*]', '', transcription)
                transcription=re.sub('[[A-Z]*]', '', transcription)
                e['transcription'] = transcription
                e['sentence_path']=path_to_sentences+f+'/'+e['id']+'.wav'
                e['speaker']=session+'_'+e['id'][-4]
                data.append(e)

    # data = np.array(data)
    # pdb.set_trace()
    data=pd.DataFrame.from_records(data)

    # print(data)
    print(len(data))
    return data

######################################################

import glob
def load_libri(path_to_libri='/media/adminpc/DATA/databases/LibriSpeech', category='test-clean'):
    full_path=os.path.join(path_to_libri, category)
    data=[]
    # read directory list by speaker
    speaker_list = glob.glob(full_path + '/*')
    for spk in speaker_list:
        # read directory list by chapter
        chapter_list = glob.glob(spk + '/*/')
        for chap in chapter_list:

            # read label text file list
            file_list = glob.glob(chap + '/*.wav')
            for fpath in file_list:
                #print(fpath)
                txt=fpath[:-4]+'.normalized.txt'
                with open(txt, 'rt') as f:
                    text = f.read()
                    id=os.path.split(fpath)[1].split('.')[0]
                    #print(id)
                    e = {'database': 'LibriTTS',
                         'id': id,
                         'speaker': spk.split('/')[-1],
                         # 'emotion':emotion_categories[cat],
                         'transcription': text,
                         'sentence_path': fpath}
                    data.append(e)

    data = pd.DataFrame.from_records(data)
    return data

def pred_sphinx(path):
    t, d = stt_sphinx(path)
    e = {}
    e['text'] = t
    e['duration'] = d
    return e
def pred_google(path):
    t, d = stt_google_path(path)
    e = {}
    e['text'] = t
    e['duration'] = d
    return e
def pred_ibm(path):
    t, d = stt_ibm(path)
    e = {}
    e['text'] = t
    e['duration'] = d
    return e


# This function comes from https://github.com/Franck-Dernoncourt/ASR_benchmark/blob/master/src/metrics.py
def wer(ref, hyp ,debug=False):
    '''
    This function was originally written by SpacePineapple
    http://progfruits.blogspot.com/2014/02/word-error-rate-wer-and-word.html
    '''
    DEL_PENALTY = 1
    SUB_PENALTY = 1
    INS_PENALTY = 1
    #r = ref.split()
    #h = hyp.split()
    r= ref
    h = hyp
    #costs will holds the costs, like in the Levenshtein distance algorithm
    costs = [[0 for inner in range(len(h)+1)] for outer in range(len(r)+1)]
    # backtrace will hold the operations we've done.
    # so we could later backtrace, like the WER algorithm requires us to.
    backtrace = [[0 for inner in range(len(h)+1)] for outer in range(len(r)+1)]

    OP_OK = 0
    OP_SUB = 1
    OP_INS = 2
    OP_DEL = 3

    # First column represents the case where we achieve zero
    # hypothesis words by deleting all reference words.
    for i in range(1, len(r)+1):
        costs[i][0] = DEL_PENALTY*i
        backtrace[i][0] = OP_DEL

    # First row represents the case where we achieve the hypothesis
    # by inserting all hypothesis words into a zero-length reference.
    for j in range(1, len(h) + 1):
        costs[0][j] = INS_PENALTY * j
        backtrace[0][j] = OP_INS

    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                costs[i][j] = costs[i-1][j-1]
                backtrace[i][j] = OP_OK
            else:
                substitutionCost = costs[i-1][j-1] + SUB_PENALTY # penalty is always 1
                insertionCost    = costs[i][j-1] + INS_PENALTY   # penalty is always 1
                deletionCost     = costs[i-1][j] + DEL_PENALTY   # penalty is always 1

                costs[i][j] = min(substitutionCost, insertionCost, deletionCost)
                if costs[i][j] == substitutionCost:
                    backtrace[i][j] = OP_SUB
                elif costs[i][j] == insertionCost:
                    backtrace[i][j] = OP_INS
                else:
                    backtrace[i][j] = OP_DEL

    # back trace though the best route:
    i = len(r)
    j = len(h)
    numSub = 0
    numDel = 0
    numIns = 0
    numCor = 0
    if debug:
        print("OP\tREF\tHYP")
        lines = []
    while i > 0 or j > 0:
        if backtrace[i][j] == OP_OK:
            numCor += 1
            i-=1
            j-=1
            if debug:
                lines.append("OK\t" + r[i]+"\t"+h[j])
        elif backtrace[i][j] == OP_SUB:
            numSub +=1
            i-=1
            j-=1
            if debug:
                lines.append("SUB\t" + r[i]+"\t"+h[j])
        elif backtrace[i][j] == OP_INS:
            numIns += 1
            j-=1
            if debug:
                lines.append("INS\t" + "****" + "\t" + h[j])
        elif backtrace[i][j] == OP_DEL:
            numDel += 1
            i-=1
            if debug:
                lines.append("DEL\t" + r[i]+"\t"+"****")
    if debug:
        lines = reversed(lines)
        for line in lines:
            print(line)
        #print("#cor " + str(numCor))
        #print("#sub " + str(numSub))
        #print("#del " + str(numDel))
        #print("#ins " + str(numIns))
    #return (numSub + numDel + numIns) / (float) (len(r))
    wer_result = (numSub + numDel + numIns) / (float) (len(r))
    #return {'WER':wer_result, 'Cor':numCor, 'Sub':numSub, 'Ins':numIns, 'Del':numDel}
    return {'wer':wer_result, 'changes': numSub + numDel + numIns, 'corrects':numCor, 'substitutions':numSub, 'insertions':numIns, 'deletions':numDel, 'length ref':len(ref)}

def compute_predictions(platforms=['sphinx','google','ibm','deepspeech']):
    sphinx, google, ibm = [], [], []
    for i, row in data.iterrows():
        print('row number:')
        print(i)
        path = row.sentence_path
        if 'sphinx' in platforms:
            e = pred_sphinx(path)
            sphinx.append(e)
            if i%100==0:
                sphinx_df = pd.DataFrame.from_records(sphinx)
                sphinx_df.to_csv('pred_sphinx.csv')
        if 'google' in platforms:
            e = pred_google(path)
            google.append(e)
            if i%100==0:
                google_df = pd.DataFrame.from_records(google)
                google_df.to_csv('pred_google.csv')
        if 'ibm' in platforms:
            e = pred_ibm(path)
            ibm.append(e)
            if i%100==0:
                ibm_df = pd.DataFrame.from_records(ibm)
                ibm_df.to_csv('pred_ibm.csv')
    if 'sphinx' in platforms:
        sphinx_df = pd.DataFrame.from_records(sphinx)
        sphinx_df.to_csv('pred_sphinx.csv')
    if 'google' in platforms:
        google_df = pd.DataFrame.from_records(google)
        google_df.to_csv('pred_google.csv')
    if 'ibm' in platforms:
        ibm_df = pd.DataFrame.from_records(ibm)
        ibm_df.to_csv('pred_ibm.csv')

def isnan(n):
    return n!=n

import tqdm
import pdb


def compute_wer(ref_list, hyp_list):
    '''

    :param ref_list: reference list of strings
    :param hyp_list: predicted list of strings
    :return: a DataFrame containing the wor error rates
    '''
    pred_wer=[]
    for i in tqdm.tqdm(range(len(ref_list))):
        try:
            ref = ref_list[i].lower()
        except:
            pdb.set_trace()
        #print(i)
        #print(ref)
        hyp = hyp_list[i]
        #print(hyp)
        def res_wer(ref,hyp):
            if isnan(hyp): hyp=''
            try:
                hyp = hyp.lower()
            except:
                pdb.set_trace()
            if not ref=='':
                try:
                    res=wer(ref, hyp)
                except:
                    pdb.set_trace()
            else:
                res={}
            return res

        pred_wer.append(res_wer(ref,hyp))
    pred_wer_df = pd.DataFrame.from_records(pred_wer)
    return pred_wer_df


# This does an evaluation of different ASRs, but you need IEMOCAP dataset.
# And Also, deepspeech prediction are done with the github repo mozilla/deepspeech saved to a csv, See asr_deepspeech.py
# and here we load these results to omute wer
if __name__ == "__main__":
    data=load_iemocap()

    compute_predictions(platforms=['sphinx'])

    google = pd.read_csv('pred_google.csv')
    google_wer_df=compute_wer(data.transcription.to_list(), google.text.to_list())

    sphinx = pd.read_csv('pred_sphinx_all.csv')
    sphinx_wer_df=compute_wer(data.transcription.to_list(), sphinx.text.to_list())

    # This was computed on google colab and for some reason, it didn't load IEMOCAP files in the same
    # order. So I have to resort both data and deepspeech in terms of 'id' to have the pairs (truth, prediction)
    deepspeech = pd.read_csv('pred_deepspeech_id.csv')
    deepspeech=deepspeech.sort_values('id')
    deepspeech.index = range(len(deepspeech))
    deepspeech_wer_df = compute_wer(data.sort_values('id').transcription.to_list(), deepspeech.sort_values('id').text.to_list())

    print(google_wer_df.dropna().mean())
    print(sphinx_wer_df.dropna().mean())
    print(deepspeech_wer_df.dropna().mean())

    google.text.to_list()