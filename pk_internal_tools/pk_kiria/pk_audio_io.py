import collections
import logging
import queue
import threading
import time
import uuid
import wave

import pyaudio
from google.cloud import speech # This might require google-cloud-speech to be installed
# from google.cloud.speech_v2 import SpeechClient # newer version of google-cloud-speech
# from google.cloud.speech_v2.types import cloud_speech as speech_v2_types

# from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
from pk_internal_tools.pk_objects.pk_colors import PkColors


# Lazy import for ensure_pk_system_log_initialized
from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized

# Initialize logging for this module
ensure_pk_system_log_initialized(__file__)
logger = logging.getLogger(__name__)


# Audio configuration
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class AudioInput:
    """
    Represents a stream of audio data, either from a microphone or a file.
    It manages the collection of audio chunks into a buffer.
    """

    def __init__(self, rate: int = RATE, chunk_size: int = CHUNK, input_device_index: int = None):
        self._rate = rate
        self._chunk_size = chunk_size
        self._input_device_index = input_device_index
        self._buff = queue.Queue()
        self.closed = True
        logger.info("AudioInput initialized.")

    def __enter__(self):
        self.closed = False
        logger.info("AudioInput context entered.")
        return self

    def __exit__(self, type, value, traceback):
        self.closed = True
        logger.info("AudioInput context exited.")
        self._buff.put(None)  # Signal the generator to stop

    def _generator(self):
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
            yield b''.join(data)

    def start_recording(self):
        """Starts recording from the microphone in a separate thread."""
        logger.info("Starting audio recording from microphone.")
        self._audio = pyaudio.PyAudio()
        self._stream = self._audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk_size,
            input_device_index=self._input_device_index,
            stream_callback=self._stream_callback
        )
        self._stream.start_stream()
        logger.info(f"Microphone stream started. Device index: {self._input_device_index if self._input_device_index is not None else 'default'}")

    def stop_recording(self):
        """Stops the microphone recording."""
        if hasattr(self, '_stream') and self._stream.is_active():
            self._stream.stop_stream()
            self._stream.close()
            self._audio.terminate()
            logger.info("Microphone stream stopped and audio interface terminated.")

    def _stream_callback(self, in_data, frame_count, time_info, status):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def get_audio_chunks(self):
        return self._generator()

    def get_input_device_info(self):
        """Lists available audio input devices."""
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        devices = []
        for i in range(0, num_devices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                device_info = p.get_device_info_by_host_api_device_index(0, i)
                devices.append({
                    "index": device_info.get('index'),
                    "name": device_info.get('name'),
                    "channels": device_info.get('maxInputChannels')
                })
        p.terminate()
        return devices

class StreamedAudioInput(AudioInput):
    """
    An AudioInput that specifically handles streaming audio for real-time processing.
    It uses a RingBuffer to manage a fixed-size window of recent audio.
    """

    def __init__(self, rate: int = RATE, chunk_size: int = CHUNK, input_device_index: int = None, ring_buffer_size_ms: int = 3000):
        super().__init__(rate, chunk_size, input_device_index)
        self._ring_buffer = collections.deque(
            maxlen=int(rate * ring_buffer_size_ms / (1000 * chunk_size))
        )
        logger.info(f"StreamedAudioInput initialized with ring buffer size {ring_buffer_size_ms}ms.")

    def _stream_callback(self, in_data, frame_count, time_info, status):
        self._buff.put(in_data)
        self._ring_buffer.append(in_data)
        return None, pyaudio.paContinue

    def get_latest_audio(self) -> bytes:
        """Returns the concatenated audio from the ring buffer."""
        return b''.join(self._ring_buffer)


class AudioPlayer:
    """
    Plays back audio data through the system's default audio output.
    """

    def __init__(self, rate: int = RATE):
        self._rate = rate
        self._audio = pyaudio.PyAudio()
        self._stream = self._audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            output=True
        )
        logger.info("AudioPlayer initialized.")

    def play(self, audio_data: bytes):
        """Plays the given raw audio data."""
        logger.info(f"Playing audio data of length {len(audio_data)} bytes.")
        self._stream.write(audio_data)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._stream.stop_stream()
        self._stream.close()
        self._audio.terminate()
        logger.info("AudioPlayer stream stopped and audio interface terminated.")


def send_mic_audio(config: speech.RecognitionConfig, audio_input: AudioInput, client: speech.SpeechClient):
    """
    Sends microphone audio to Google Speech-to-Text API.
    """
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_input.get_audio_chunks()
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    logger.info(f"{PkColors.BRIGHT_CYAN}Sending mic audio for STT...{PkColors.RESET}")
    responses = client.streaming_recognize(streaming_config, requests)

    # Now, handle the responses in real-time
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        alternative = result.alternatives[0]
        logger.info(f"Transcript: {alternative.transcript}")
        if result.is_final:
            logger.info(f"{PkColors.BRIGHT_GREEN}Final Transcript: {alternative.transcript}{PkColors.RESET}")
            return alternative.transcript
    return None

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # Example usage:
    # List audio input devices
    logger.info("Available audio input devices:")
    audio_devices = AudioInput().get_input_device_info()
    for dev in audio_devices:
        logger.info(f"{dev}")

    # Set a specific device index if available, otherwise use default (None)
    # input_device_index = audio_devices[0]['index'] if audio_devices else None
    input_device_index = None # Using default for example

    # Record and play back for a few seconds
    logger.info("Recording for 5 seconds and playing back...")
    recorded_chunks = []
    with AudioInput(input_device_index=input_device_index) as audio_input:
        audio_input.start_recording()
        start_time = time.time()
        while (time.time() - start_time) < 5:
            try:
                chunk = audio_input._buff.get(timeout=0.1) # Accessing internal buffer for simple example
                recorded_chunks.append(chunk)
            except queue.Empty:
                pass
        audio_input.stop_recording()

    full_audio = b''.join(recorded_chunks)
    logger.info(f"Recorded {len(full_audio)} bytes of audio.")

    with AudioPlayer() as audio_player:
        audio_player.play(full_audio)
    logger.info("Playback finished.")

    # Example of StreamedAudioInput (for continuous processing)
    # In a real scenario, this would be hooked up to an STT service continuously
    logger.info("Starting StreamedAudioInput for 10 seconds (check ring buffer functionality)...")
    with StreamedAudioInput(input_device_index=input_device_index, ring_buffer_size_ms=2000) as streamed_audio_input:
        streamed_audio_input.start_recording()
        start_time = time.time()
        while (time.time() - start_time) < 10:
            time.sleep(0.5) # Simulate processing intervals
            latest_audio = streamed_audio_input.get_latest_audio()
            logger.info(f"StreamedAudioInput: Latest {len(latest_audio)} bytes from ring buffer.")
        streamed_audio_input.stop_recording()
    logger.info("StreamedAudioInput test finished.")