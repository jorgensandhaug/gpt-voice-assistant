# play a file using scipy
from scipy.io import wavfile
import sounddevice as sd
import numpy as np
import time


def play(filename):
    # Print now playing message
    print("Now playing: " + filename)

    # Read the audio file
    rate, data = wavfile.read(filename)

    # Play the audio file
    sd.play(data, rate)

    # Wait until the file is done playing
    status = sd.wait()


    # Print stopped playing message
    print("Stopped playing: " + filename)

