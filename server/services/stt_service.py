"""Streaming microphone Speech-to-Text using Google Cloud Speech.

Provides a context manager `MicrophoneStream` to capture audio from the
system microphone and a `transcribe` function that performs streaming
recognition with voice-activity end timeout.

Requirements:
- PyAudio for audio capture
- Google Cloud credentials via `GOOGLE_APPLICATION_CREDENTIALS`
"""

import queue

from google.cloud import speech
from google.protobuf import duration_pb2

import pyaudio

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

TIMEOUT = duration_pb2.Duration()
TIMEOUT.seconds = 1

class MicrophoneStream:
    """Context manager that captures microphone audio and yields byte chunks.

    The audio capture runs asynchronously and collected frames are exposed via
    a thread-safe queue. Use the `generator()` to iterate audio chunks.

    Args:
        rate (int): Sample rate in Hz. Defaults to RATE.
        chunk (int): Frames per buffer to read from the device.
    """

    def __init__(self: object, rate: int = RATE, chunk: int = CHUNK) -> None:
        """The audio -- and generator -- is guaranteed to be on the main thread."""
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self: object) -> object:
        """Open the PyAudio stream and start collecting audio frames.

        Returns:
            MicrophoneStream: The active stream context.
        """
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(
        self: object,
        type: object,
        value: object,
        traceback: object,
    ) -> None:
        """Close the audio stream and signal the generator to finish."""
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(
        self: object,
        in_data: object,
        frame_count: int,
        time_info: object,
        status_flags: object,
    ) -> object:
        """Collect data from the device into the internal buffer.

        Args:
            in_data (bytes): Raw audio bytes provided by PyAudio callback.
            frame_count (int): Number of frames captured.
            time_info (object): Timestamp metadata from PyAudio.
            status_flags (object): Status flags from PyAudio.

        Returns:
            tuple: (None, pyaudio.paContinue) per PyAudio callback contract.
        """
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self: object) -> object:
        """Yield concatenated audio byte chunks until the stream is closed.

        Returns:
            Generator[bytes, None, None]: Iterator over raw audio chunks.
        """
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

def listen_print_loop(responses: object) -> str:
    """Consume streaming recognition responses and return the final transcript.

    Iterates over streaming responses until a final result is produced, then
    returns the top alternative's transcript.

    Args:
        responses (Iterable): StreamingRecognize responses iterator.

    Returns:
        str: Final transcribed text for the current utterance.
    """
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        if result.is_final:
            return transcript
    
def transcribe(language: str = "en-US") -> str:
    """Perform streaming speech recognition from the default microphone.

    Opens a `MicrophoneStream`, sends audio to Google Cloud Speech with
    automatic punctuation and a short voice-activity end timeout, and returns
    the first finalized transcript.

    Args:
        language (str): BCP‑47 language code (e.g., "en-US", "fr-FR").

    Returns:
        str: The recognized text for the user's utterance.
    """
    language_code = language

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, 
        interim_results=True, 
        voice_activity_timeout= speech.StreamingRecognitionConfig.VoiceActivityTimeout(mapping=None, speech_end_timeout = TIMEOUT, ignore_unknown_fields=False)
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        transcript = listen_print_loop(responses)
        print(transcript)
        return transcript

if __name__ == "__main__":
    transcribe("fr-FR")