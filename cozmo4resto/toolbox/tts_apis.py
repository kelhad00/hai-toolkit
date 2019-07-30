# IBM text to speech in python
# source: https://cloud.ibm.com/apidocs/speech-to-text?code=python
# after creating a tts resource, go to https://cloud.ibm.com/resources
def tts_ibm(text='Hello, this is a first system to synthesize speech with IBM API',
            apikey='ebUiBwxYZwRw_2dyt-3vi0QeHhlKbT0tLgfZOC3aokxu',
            url='https://gateway-lon.watsonplatform.net/text-to-speech/api',
            save=False, path='tts_ibm/test.wav'):
    from ibm_watson import TextToSpeechV1

    text_to_speech = TextToSpeechV1(
        iam_apikey=apikey,
        url=url
    )

    speech_bytes = text_to_speech.synthesize(
        text,
        voice='en-US_AllisonVoice',
        accept='audio/mp3'
    ).get_result()  # .content

    if save:
        with open(path, 'wb') as audio_file:
            audio_file.write(speech_bytes.content)

    # Write
    print(len(speech_bytes.content))
    from pygame import mixer
    from tempfile import TemporaryFile
    sf = TemporaryFile()

    for chunk in speech_bytes.iter_content():
        sf.write(chunk)

    sf.seek(0)
    mixer.init()
    mixer.music.load(sf)
    mixer.music.play()

    return speech_bytes


# source: https://github.com/guillochon/MOSFiT/blob/master/mosfit/utils.py
def gtts(text='hello', save=False, path='gtts/test.mp3'):
    from gtts import gTTS
    tts = gTTS(text, 'en')

    if save:
        tts.save(path)
    from pygame import mixer
    from tempfile import TemporaryFile

    mixer.init()

    sf = TemporaryFile()
    tts.write_to_fp(sf)
    sf.seek(0)
    mixer.music.load(sf)
    mixer.music.play()

    return tts

if __name__ == "__main__":
    text_file = open("harvsents.txt", "r")
    lines = text_file.readlines()

    for i,l in enumerate(lines):
        folder='gtts'
        if not os.path.exists(folder): os.makedirs(folder)
        gtts(l.replace('\n',''), save=True, path=os.path.join(folder,str(i)+'.mp3'))

        folder='tts_ibm'
        if not os.path.exists(folder): os.makedirs(folder)
        tts_ibm(l.replace('\n',''), save=True, path=os.path.join(folder,str(i)+'.wav'))

