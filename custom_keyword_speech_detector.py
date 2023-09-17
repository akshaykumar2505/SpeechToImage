import time
import wave

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)

speech_key, service_region = "358042514ae140d99369f009fedbbe52", "eastus"

def speech_recognize_keyword_locally_from_microphone():

    model = speechsdk.KeywordRecognitionModel("custom_keyword_speech_model.table")

    keyword = "Hello Nightfall"

    keyword_recognizer = speechsdk.KeywordRecognizer()

    done = False

    def recognized_cb(evt):
        result = evt.result
        if result.reason == speechsdk.ResultReason.RecognizedKeyword:
            print("RECOGNIZED KEYWORD: {}".format(result.text))
        nonlocal done
        done = True

    def canceled_cb(evt):
        result = evt.result
        if result.reason == speechsdk.ResultReason.Canceled:
            print('CANCELED: {}'.format(result.cancellation_details.reason))
        nonlocal done
        done = True

    keyword_recognizer.recognized.connect(recognized_cb)
    keyword_recognizer.canceled.connect(canceled_cb)

    result_future = keyword_recognizer.recognize_once_async(model)
    print('Say something starting with "{}" followed by whatever you want...'.format(keyword))
    result = result_future.get()

    if result.reason == speechsdk.ResultReason.RecognizedKeyword:
        time.sleep(10)
        result_stream = speechsdk.AudioDataStream(result)
        result_stream.detach_input() 

        save_future = result_stream.save_to_wav_file_async("AudioFromRecognizedKeyword.wav")
        print('Saving file...')
        saved = save_future.get()
          
speech_recognize_keyword_locally_from_microphone()        