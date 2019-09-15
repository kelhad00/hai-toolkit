# hai-toolkit
Open-source HAI toolkit

# Source Localization


# Text to Speech Synthesis - TTS

`pip install -r requirements_TTS.txt`

* [IBM watson](https://cloud.ibm.com/apidocs/speech-to-text?code=python)

after creating a tts resource, go to https://cloud.ibm.com/resources
Then take the corresponding API key and paste it in tts_apis

* gTTS (using google translate's synthesizer)
* pyttsx3

# Automatic Speech Recognition - ASR

* [IBM watson](https://cloud.ibm.com/apidocs/speech-to-text?code=python)

after creating a stt resource, go to https://cloud.ibm.com/resources
get the API key and write it in asr_apis.py

* Google Speech recognition API

* [DeepSpeech](https://cloud.ibm.com/apidocs/speech-to-text?code=python)

------------------------
For GPU version:
deepspeeh-gpu:
https://github.com/mozilla/DeepSpeech#cuda-dependency

Install cudnn version 7.6, and cudatoolkit 10.0

`conda install cudnn=7.6.0 cudatoolkit=10.0`

Then install deepspeech:

`pip install deepspeech-gpu`

-----------------------
For CPU version:

`pip install deepspeech`

------------------------


* Sphinx

# Keyword Spotting - KWS

We make use of [this repository](https://github.com/Picovoice/wakeword-benchmark).

Clone this in the same folder as toolbox/mic_aqui_kws.py with the name "kws"

* Snowboy
* Porcupine

# Dialog Management - DM

`pip install rasa`

[Documentation on RASA](https://rasa.com/docs/rasa/)

For now, you can connect the DM to a Google Connector. How? Like this:

* add connector to credentials.py
* start project on [Google Actions](https://console.actions.google.com)
* run rasa with following command: `rasa run --enable-api -p #PORT#`
* start ngrok server: `ngrok http #SAMEPORT#`
* start rasa actions on different server: `rasa run actions`
* start Google Actions: `gactions test --action_package action.json --project #PROJECTNAME#
