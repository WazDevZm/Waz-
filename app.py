import whisper
import sounddevice as sd
import numpy as np
import queue
import ollama
from elevenlabs.client import ElevenLabs
from elevenlabs import stream

class WazDevVoiceAssistant:
    def __init__(self):
        self.client = ElevenLabs(
            api_key="sk_2a9cf2cd64b1f762628f8983978f34289e44aad3cf6b4cb2"
        )
        self.model = whisper.load_model("base")  # Use "tiny" for faster performance
        self.audio_queue = queue.Queue()
        self.samplerate = 16000  # Sample rate for recording
        self.full_transcript = [
            {"role": "system", "content": "You are a language model called WazDevVoiceAssistant"}
        ]

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Audio error: {status}")
        self.audio_queue.put(indata.copy())  # Store audio in queue

    def start_transcription(self):
        print("\nReal-time transcription started...")
        with sd.InputStream(samplerate=self.samplerate, channels=1, callback=self.audio_callback):
            while True:
                audio_data = self.audio_queue.get()
                audio_data = audio_data.flatten()  # Convert to 1D numpy array
                result = self.model.transcribe(audio_data)
                transcript = result["text"].strip()

                if transcript:
                    print("\nUser:", transcript)
                    self.generate_ai_response(transcript)

    def generate_ai_response(self, transcript):
        self.full_transcript.append({"role": "user", "content": transcript})

        print("\nGenerating AI response...")
        ollama_stream = ollama.chat(
            model="deepseek-r1:7b",
            messages=self.full_transcript,
            stream=True,
        )

        print("\nDeepSeek R1 Response:")
        text_buffer = ""
        full_text = ""

        for chunk in ollama_stream:
            if "message" in chunk and "content" in chunk["message"]:
                text_buffer += chunk["message"]["content"]
                if len(text_buffer) > 50 or text_buffer.endswith("."):
                    audio_stream = self.client.generate(
                        text=text_buffer,
                        model="eleven_turbo_v2",
                        stream=True
                    )
                    print(text_buffer, flush=True)
                    stream(audio_stream)
                    full_text += text_buffer
                    text_buffer = ""

        if text_buffer:
            audio_stream = self.client.generate(
                text=text_buffer,
                model="eleven_turbo_v2",
                stream=True
            )
            print(text_buffer, flush=True)
            stream(audio_stream)
            full_text += text_buffer

        self.full_transcript.append({"role": "assistant", "content": full_text})

if __name__ == "__main__":
    ai_voice_agent = WazDevVoiceAssistant()
    ai_voice_agent.start_transcription()
