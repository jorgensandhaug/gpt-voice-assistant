from api import chat, start_browser 
from tts import text_to_audio
from record_audio import record
from play_audio import play
from transcribe import transcribe

    
    

template = "$chat\nPlease respond as concisely as possible, and dont reply with anything other than the concrete response."

if __name__ == "__main__":
    start_browser()
    while True:
        record()
        message = transcribe("output.mp3")
        response = chat(template.replace("$chat", message))
        #print(response)
        text_to_audio(response)