import whisper
from threading import Thread

# Use fmpeg to create an audio file from the microphone input stream
# Use the following command to install ffmpeg on Ubuntu
# sudo apt-get install ffmpeg
# Path: audio.py
import pyaudio
import wave

chunk = 1024
thread_running = True


def record():
    global thread_running, chunk
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

# Play audio
def play(filename):
    global chunk
    wf = wave.open(filename, 'rb')

    p = pyaudio.PyAudio()



    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunk)

    #Print now playing message
    print("Now playing: " + filename)

    # WHile data not empty
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()

    # Print stopped playing message
    print("Stopped playing: " + filename)





if __name__ == "__main__":
    # Initialize the threads
    record_thread = Thread(target=record)
    input_thread = Thread(target=record_input)

    # print the instructions
    print("Press f to stop recording")

    # Start the threads
    record_thread.start()
    input_thread.start()

    # Wait for the threads to finish
    record_thread.join()

    # Play the audio file
    play("output.wav")
    

    # Set options
    options = dict(language="english", beam_size=5, best_of=5)
    translate_options = dict(task="translate", **options)

    # Transcribe the audio file
    # Print now transcribing message
    print("Now transcribing: output.wav")
    model = whisper.load_model("large-v2")
    result = model.transcribe("output.wav", **translate_options)
    print("Transcribed result", result["text"])

    # Write result to file
    with open("result.txt", "w") as f:
        f.write(result["text"])

    # Print stopped transcribing message
    print("Stopped transcribing: output.wav")

    
    




