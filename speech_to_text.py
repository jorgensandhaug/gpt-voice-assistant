import whisper
from threading import Thread

# Use fmpeg to create an audio file from the microphone input stream
# Use the following command to install ffmpeg on Ubuntu
# sudo apt-get install ffmpeg
# Path: audio.py
import pyaudio
import wave

thread_running = True


def record():
    global thread_running
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100
    seconds = 10
    filename = "output.wav"

    p = pyaudio.PyAudio()

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    # Read the data in chunks until the user presses f
    while thread_running:
        data = stream.read(chunk)
        frames.append(data)


    stream.stop_stream()
    stream.close()
    p.terminate()

    print('Finished recording')

    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(p.get_sample_size(sample_format))
    waveFile.setframerate(fs)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


# Takes input from user and if the user presses f, it stops recording
def record_input():
    global thread_running
    while True:
        if input() == 'f':
            thread_running = False
            break

# Then create a function to play audio
def play(filename):
    chunk = 1024
    wf = wave.open(filename, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunk)

    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()

    # Print stop recording
    print('Finished playing')


model = whisper.load_model("medium")
def transcribe(filename):
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(filename)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions(fp16 = False)
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)

if __name__ == "__main__":
    # Initialize the threads
    record_thread = Thread(target=record)
    input_thread = Thread(target=record_input)

    # Start the threads
    record_thread.start()
    input_thread.start()

    # Wait for the threads to finish
    record_thread.join()


    #play("output.wav")
    transcribe(filename="output.wav")


