from gtts import gTTS
import speech_recognition as sr

def asr():
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        audio = rec.record(source, 5)
    text = rec.recognize_google(audio)
    return text

def tts(text):
    name = str(uuid.uuid4().int)[:10]
    tts = gTTS(text, 'en')
    tts.save('potato_'+name+'.wav')

def dm(input):
    dct = {'potato':'coconut', 'banana':'papaya'}
    try:
        output = dct[input]
    except:
        output = "Nothing I know!"
    return output