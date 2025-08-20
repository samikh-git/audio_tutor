"""Text-to-Speech service using ElevenLabs streaming API.

Loads the ElevenLabs client from environment variables and provides a `speak`
function to stream synthesized audio for a given script in a selected
language. Voice IDs are mapped per supported language.
"""
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import os

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

voices  = {
    "Mandarin": "bhJUNIXWQQ94l8eI2VUf",
    "French": "sANWqF1bCMzR6eyZbCGw",
    "Spanish": "Nh2zY9kknu6z4pZy6FhD",
    "Japanese": "cgSgspJ2msm6clMCkdW9",
    "German": "z1EhmmPwF0ENGYE8dBE6",
    "Italian": "gfKKsLN1k0oYYN9n2dXX",
    "English": "JBFqnCBsd6RMkjVDRZzb"
}

def speak(script: str, language: str = "English"):
    """Stream synthesized speech for the provided text.

    Args:
        script (str): Text for the voice to read.
        language (str): One of the keys defined in `voices` mapping.

    Raises:
        KeyError: If the language is not in the `voices` mapping.
    """
    audio_stream = elevenlabs.text_to_speech.stream(
        text= script,
        voice_id= voices[language],
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128",
    )
    stream(audio_stream)

if __name__ == "__main__":
    speak("Hey There!")