import whisper

# Set options
options = dict(language="english", beam_size=5, best_of=5, fp16=False)
translate_options = dict(task="translate", **options)

def transcribe(fileName):
    # Transcribe the audio file
    # Print now transcribing message
    print("Now transcribing: " + fileName)


    model = whisper.load_model("large")
    result = model.transcribe(fileName, **translate_options)
    print("Transcribed result", result["text"])
    # Print stopped transcribing message
    print("Stopped transcribing: " + fileName)
    return result["text"]

if __name__ == "__main__":
    print(transcribe("output.mp3"))
