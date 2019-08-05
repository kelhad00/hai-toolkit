import speech_recognition as sr


def asr(inputs=None):
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        audio = rec.record(source, 5)
    text = rec.recognize_google(audio)
    return text