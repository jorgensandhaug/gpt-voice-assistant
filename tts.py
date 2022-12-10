import os
import azure.cognitiveservices.speech as speechsdk

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region="westeurope")
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name='en-US-JennyNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

xml = """
<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="en-US"
xmlns:mstts="https://www.w3.org/2001/mstts">
  <voice name="en-US-DavisNeural">
    <mstts:express-as style="chat">
        <prosody rate="+50.00%">
            $text
        </prosody>
    </mstts:express-as>
  </voice>
</speak>
"""

def text_to_audio(text):
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(xml.replace("$text", text)).get()
    
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")


