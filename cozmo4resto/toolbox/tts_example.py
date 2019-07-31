from tts_apis import *
import time


gtts('Hello world, how are you doing?')
time.sleep(3)

tts_ibm('Hello world, how are you doing?')
time.sleep(3)

import pyttsx3
engine = pyttsx3.init()
engine.say("I will speak this text")
engine.runAndWait()