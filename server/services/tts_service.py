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

language_codes = {
    "en-UK": "English",
    "fr-FR": "French",
    "es-ES": "Spanish",
    "cmn-HANS-CN": "Mandarin",
    "ja-JP": "Japanese",
    "German": "de-DE",
    "Italian": "it-IT"
}

def cli_speak(script: str, language: str = "English"):
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

def ws_speak(script: str, language_code: str = "English"): 
    """Generate streaming audio for WebSocket-based text-to-speech.

    Converts text to speech using ElevenLabs API and returns a streaming audio
    response suitable for WebSocket transmission. This function is designed for
    real-time audio streaming in WebSocket applications, returning the audio
    stream without playing it locally.

    Args:
        script (str): Text content to be converted to speech
        language_code (str): BCP-47 language code that maps to a voice ID
                           (e.g., "en-UK", "fr-FR", "es-ES")

    Returns:
        Generator: Streaming audio data in MP3 format (44100Hz, 128kbps)
                  that can be sent directly over WebSocket

    Raises:
        KeyError: If the language_code is not found in the language_codes mapping
        Exception: If there are issues with the ElevenLabs API connection

    Note:
        This function maps BCP-47 language codes to ElevenLabs voice IDs and
        returns the audio stream without playing it, unlike the speak() function
        which plays audio locally.
    """
    language = language_codes[language_code]
    return elevenlabs.text_to_speech.stream(
        text= script,
        voice_id= voices[language],
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128",
    )

if __name__ == "__main__":
    cli_speak("Hey There!")