import numpy as np
import torchaudio
from speechbrain.pretrained import Tacotron2
from speechbrain.pretrained import HIFIGAN
from play_audio import play

# Intialize TTS (tacotron2) and Vocoder (HiFIGAN)
tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="tmpdir_tts")
hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder")

def text_to_audio(text):
    # Running the TTS
    mel_output, mel_length, alignment = tacotron2.encode_text(text)

    # Running Vocoder (spectrogram-to-waveform)
    waveforms = hifi_gan.decode_batch(mel_output)

    # Save the waverform as mp3 file using .mp3 extension
    torchaudio.save("tts.wav", waveforms.squeeze(1), tacotron2.hparams.sample_rate)
    # return "Saved to " + 'tts.wav'


    

if __name__ == "__main__":
    text_to_audio("Hello world. My name is Speechbrain. I am a speech to text and text to speech model.")
    play("tts.wav")
