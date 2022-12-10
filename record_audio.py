import speech_recognition as sr
from pydub import AudioSegment

# create a recognizer object
r = sr.Recognizer()
m = sr.Microphone()
# with m as source:
#     r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
# adjust the energy threshold to filter out noise
r.energy_threshold = 3000
r.phrase_threshold = 0.3
 # self.energy_threshold = 300  # minimum audio energy to consider for recording
r.dynamic_energy_threshold = False

# self.dynamic_energy_adjustment_damping = 0.15
# self.dynamic_energy_ratio = 1.5
# self.pause_threshold = 0.8  # seconds of non-speaking audio before a phrase is considered complete
# self.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout

#  self.phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
# self.non_speaking_duration = 0.5  # seconds of non-speaking audio to keep on both sides of the recording

def record():

    # start recording audio
    with m as source:
        print("Recording audio...")
        # listen for when the speaking starts, then start recording
        # When the speaker stops speaking, stop recording
        audio = r.listen(source)

        # save the audio file
        with open("output.wav", "wb") as f:
            f.write(audio.get_wav_data())
            f.close()  
        # Convert wav to mp3
        # Open the WAV file
        sound = AudioSegment.from_file("output.wav")
        
        # Save the file as MP3
        sound.export("output.mp3", format="mp3")