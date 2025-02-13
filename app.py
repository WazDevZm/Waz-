#Building my own AI system from s`ratch#
#Dracula extension
import assemblyai as aai
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import ollama

class WazDevVoiceAssistant:
    def __init__(self):
        aai.settings.api_key = "Wazingwa"
        self.client = ElevenLabs(
            api_key= "Wazingwa"
        )
        
        self.transcriber = None
        
        self.full_transcipt = [
            {"role" : "system" , "content" : "Your are a language model called WazDevVoiceAssistant"}
        ]
    def start_transcription(self):
        print(f"\nReal-time transcription: ", end="\r\n")
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate=16_000,
            on_data=self.on_data,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close,
        )
        
        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16_000)
        self.transcriber.stream(microphone_stream)
        
    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None
    
    def on_open()