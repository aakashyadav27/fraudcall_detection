from flask import Flask, request, jsonify, render_template,make_response
import os
import time
import azure.cognitiveservices.speech as speechsdk
import requests, uuid, json
app = Flask(__name__)
result=''

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/hello',methods=['GET'])
def hello_w():
    return "hello world"
@app.route('/start',methods=['POST'])
def continous_reg():
    path = os.getcwd()
    done = False

    def collectResult(evt):
        global result
        print("Recognized")
        result += evt.result.text



    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: collectResult(evt))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    recognition = speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)


@app.route('/end', methods=['POST'])
def stop_cb():
    speech_recognizer.stop_continuous_recognition()
    body={'text':result}
    #request = requests.post(constructed_url, params=params, headers=headers, json=body)
    #response = request.json()
    #json.dumps(body, sort_keys=True, indent=4, separators=(',', ': '))
    return make_response(result)








"""def recognize_from_mic():
    speech_config = speechsdk.SpeechConfig(subscription="63453a65ffa9493aac460355cffdfa9a", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    # Asks user for mic input and prints transcription result on screen
    print("Speak into your microphone.")
    #Performs recognition in a blocking (synchronous) mode. Returns after a single utterance is recognized.
    # The end of a single utterance is determined by listening for silence at the end or until a maximum of 15 seconds
    # of audio is processed.
    result = speech_recognizer.recognize_once_async().get()
    #print(result.reason)
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        result_1="Recognized: {}".format(result.text)
    elif result.reason == speechsdk.ResultReason.NoMatch:
        result_1="No speech could be recognized: {}".format(result.no_match_details)
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        result_1 ="Speech Recognition canceled: {}".format(cancellation_details.reason)
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            result_1 ="Error details: {}".format(cancellation_details.error_details)
    return render_template('index.html', prediction_text='transcription: {}'.format(result_1))"""

if __name__ == "__main__":
    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
    speech_key, service_region = "42a993a2322a45089212aa9a9cedd520", "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates a recognizer with the given settings
    speech_config.speech_recognition_language = "hi-IN"
    # source_language_config = speechsdk.languageconfig.SourceLanguageConfig("en-US", "The Endpoint ID for your custom model.")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)


    # Add your subscription key and endpoint
    subscription_key = "5a465e70f4b1416c86d44a5839b9d660"
    endpoint = "https://api.cognitive.microsofttranslator.com/"

    # Add your location, also known as region. The default is global.
    # This is required if using a Cognitive Services resource.
    location = "eastus"

    path = '/transliterate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'language': 'hi',
        'fromScript': 'Deva',
        'toScript': 'latn'
    }

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    app.run(debug=True)