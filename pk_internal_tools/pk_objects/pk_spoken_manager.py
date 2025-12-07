import queue
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from pk_internal_tools.pk_objects import pk_tts_cache_utils


# --- Utility Functions ---






def remove_special_characters(text):
    """특수문자를 제거합니다."""
    return ''.join(e for e in text if e.isalnum() or e.isspace())


# --- Configuration ---
@dataclass
class VoiceConfig:
    """음성 설정"""
    name: str = "기본 음성"
    rate: int = 150
    volume: float = 0.8
    voice_id: Optional[str] = None
    language: str = "ko"
    gender: str = "male"


# --- Abstractions (Backends and Player) ---
class TTSBackend(ABC):
    """TTS 백엔드의 추상 기반 클래스"""

    def __init__(self, cache_dir: str, verbose: bool = True):
        import os
        self.verbose = verbose
        self._cache_dir = cache_dir
        os.makedirs(self._cache_dir, exist_ok=True)

    @abstractmethod
    def synthesize(self, text: str, voice_config: VoiceConfig) -> Optional[str]:
        """텍스트를 음성으로 합성하고 오디오 파일 경로를 반환합니다."""
        pass

    def _verify_mp3(self, file_path: str) -> bool:
        import os
        import logging
        """MP3 파일의 무결성을 검증합니다."""
        try:
            from mutagen.mp3 import MP3, MutagenError
        except ImportError:
            if self.verbose: logging.warning("Mutagen library not found, skipping MP3 verification.")
            return os.path.exists(file_path) and os.path.getsize(file_path) > 0

        try:
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                if self.verbose: logging.debug(f"[VERIFY_MP3] FAILED: File does not exist or is empty at {file_path}")
                return False
            audio = MP3(file_path)
            if self.verbose: logging.info(f"[VERIFY_MP3] SUCCESS: Duration: {audio.info.length:.2f}s. Path: {file_path}")
            return True
        except MutagenError as e:
            if self.verbose: logging.debug(f"[VERIFY_MP3] FAILED: Mutagen could not process file. Error: {e}", exc_info=True)
            return False
        except Exception as e:
            if self.verbose: logging.debug(f"[VERIFY_MP3] FAILED: Unexpected error. Error: {e}", exc_info=True)
            return False


class PygamePlayer:
    """Pygame을 사용한 오디오 재생기"""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self._current_sound = None

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def play(self, audio_file_path: str, volume: float):
        import os
        import logging
        import time
        try:
            import pygame
        except ImportError:
            if self.verbose: logging.error("Pygame is not installed, cannot play audio.")
            return False

        if not os.path.exists(audio_file_path):
            if self.verbose: logging.error(f"Audio file not found for playback: {audio_file_path}")
            return False

        try:
            sound = pygame.mixer.Sound(audio_file_path)
            self._current_sound = sound

            channel = sound.play()
            if self.verbose: logging.debug(f"PygamePlayer: sound.play() returned channel: {channel}")

            if channel is not None:
                channel.set_volume(volume)
                if self.verbose: logging.debug(f"Sound duration: {sound.get_length():.2f}s. Waiting for playback...")

                is_busy_before_loop = pygame.mixer.get_busy()
                if self.verbose: logging.debug(f"PygamePlayer: Mixer busy before loop: {is_busy_before_loop}")

                while pygame.mixer.get_busy():
                    time.sleep(0.01)

                is_busy_after_loop = pygame.mixer.get_busy()
                if self.verbose: logging.debug(f"PygamePlayer: Mixer busy after loop: {is_busy_after_loop}")

                channel.stop()
                self._current_sound = None

                if self.verbose: logging.info(f"Playback finished for {audio_file_path}")
                return True
            else:
                if self.verbose: logging.warning(f"No available channel to play {audio_file_path}.")
                self._current_sound = None
                return False
        except Exception as e:
            if self.verbose: logging.error(f"Error during pygame playback: {e}", exc_info=True)
            self._current_sound = None
            return False


# --- Backend Implementations ---
class GTTSBackend(TTSBackend):
    def synthesize(self, text: str, voice_config: VoiceConfig) -> Optional[str]:
        import os
        import logging
        try:
            from gtts import gTTS
        except ImportError:
            if self.verbose: logging.warning("gTTS is not installed, skipping.")
            return None

        from pk_internal_tools.pk_functions.is_internet_connected_2025_10_21 import is_internet_connected_2025_10_21
        if not is_internet_connected_2025_10_21():
            if self.verbose: logging.debug("No internet connection, skipping gTTS.")
            return None

        try:
            cache_path = pk_tts_cache_utils.get_cache_path_for_backend(text, voice_config, 'gtts')

            if not os.path.exists(cache_path):
                if self.verbose: logging.info(f"Creating new speech file for text: '{text[:20]}...'")
                tts = gTTS(text=text, lang=voice_config.language)
                tts.save(str(cache_path))
            else:
                if self.verbose: logging.debug(f"Using cached file.{cache_path}")

            if self._verify_mp3(cache_path):
                return cache_path
            return None
        except Exception as e:
            if self.verbose: logging.error(f"gTTS failed: {e}", exc_info=True)
            return None


class ElevenLabsBackend(TTSBackend):
    def synthesize(self, text: str, voice_config: VoiceConfig) -> Optional[str]:
        import os
        import logging
        try:
            from elevenlabs import set_api_key, generate, save
        except ImportError:
            if self.verbose: logging.debug("ElevenLabs library not found, skipping.")
            return None

        try:
            from .pk_tts_config_manager import get_pk_tts_config_manager
            config_manager = get_pk_tts_config_manager()
            if not config_manager.ensure_api_key_exists("elevenlabs"):
                if self.verbose: logging.warning("ElevenLabs API key not configured.")
                return None

            set_api_key(config_manager.get_api_key("elevenlabs"))

            cache_path = pk_tts_cache_utils.get_cache_path_for_backend(text, voice_config, 'elevenlabs')

            if not os.path.exists(cache_path):
                if self.verbose: logging.info(f"Creating new speech file for text: '{text[:20]}...'")
                audio = generate(text=text, voice="Rachel", model="eleven_multilingual_v2")
                save(audio, cache_path)
            else:
                if self.verbose: logging.debug("Using cached file.")

            if self._verify_mp3(cache_path):
                return cache_path
            return None
        except Exception as e:
            if self.verbose: logging.error(f"ElevenLabs failed: {e}", exc_info=True)
            return None


# --- Main Orchestrator ---
class SpokenManager:
    """텍스트 음성 변환 및 재생을 관리하는 오케스트레이터"""

    def __init__(self, verbose: bool = True):
        from typing import List
        import logging
        import sys
        import io


        self.verbose = verbose
        self.voice_config = VoiceConfig()
        self._cache_dir = pk_tts_cache_utils.get_pk_tts_cache_dir()

        self.player = PygamePlayer(verbose=self.verbose)
        self.backends: List[TTSBackend] = [
            GTTSBackend(self._cache_dir, verbose=self.verbose),
            ElevenLabsBackend(self._cache_dir, verbose=self.verbose)
        ]

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        try:
            import pygame
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            if self.verbose: logging.info("Pygame mixer initialized successfully in SpokenManager.")
        except pygame.error as e:
            if self.verbose: logging.error(f"Failed to initialize Pygame mixer in SpokenManager: {e}", exc_info=True)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        self._queue = queue.Queue()
        self._stop_event = threading.Event()
        self._worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self._worker_thread.start()
        if self.verbose: logging.debug("SpokenManager initialized.")

    def set_verbose(self, verbose: bool):
        import logging
        self.verbose = verbose
        self.player.set_verbose(verbose)
        for backend in self.backends:
            backend.verbose = verbose

        # Control logging levels of external TTS libraries
        gtts_logger = logging.getLogger('gtts')
        elevenlabs_logger = logging.getLogger('elevenlabs')

        if verbose:
            gtts_logger.setLevel(logging.INFO)
            elevenlabs_logger.setLevel(logging.INFO)
        else:
            gtts_logger.setLevel(logging.WARNING)
            elevenlabs_logger.setLevel(logging.WARNING)

    def _process_queue(self):
        import queue
        while not self._stop_event.is_set():
            try:
                text = self._queue.get(timeout=1)
                self._speak_internal(text)
                self._queue.task_done()
            except queue.Empty:
                continue

    def _speak_internal(self, text: str):
        import logging
        if not text or not text.strip():
            if self.verbose: logging.warning("Speak request with empty text received.")
            return

        if self.verbose: logging.info(f"🔊 Processing speak request for: '{text[:30]}...'")

        for backend in self.backends:
            try:
                audio_path = backend.synthesize(text, self.voice_config)
                if audio_path:
                    if self.verbose: logging.info(f"Synthesized successfully with {backend.__class__.__name__}.")
                    self.player.play(audio_path, self.voice_config.volume)
                    return
            except Exception as e:
                if self.verbose: logging.error(f"Backend {backend.__class__.__name__} failed: {e}", exc_info=True)

        if self.verbose: logging.error("All TTS backends failed to synthesize text.")

    def speak(self, text: str):
        """텍스트를 FIFO 큐에 추가하여 순차적으로 재생합니다."""
        self._queue.put(text)

    def wait_for_completion(self):
        """큐의 모든 작업이 완료될 때까지 기다립니다."""
        self._queue.join()

    def set_voice_config(self, config: VoiceConfig):
        import logging
        self.voice_config = config
        if self.verbose: logging.info(f"Voice config changed to: {config.name}")

    def get_available_voices(self) -> Dict[str, List[Dict[str, Any]]]:
        return {
            "elevenlabs": [{"name": "Rachel", "id": "Rachel", "languages": ["en"]}],
            "gtts": [{"name": "Google TTS", "id": "ko", "languages": ["ko", "en"]}]
        }

    def terminate(self):
        import logging
        """FIFO 큐 처리를 중지하고 스레드를 종료합니다."""
        import pygame
        if not self._stop_event.is_set():
            self._stop_event.set()
            self._worker_thread.join(timeout=2)
            if self.verbose: logging.info("SpokenManager terminated.")
            if pygame.mixer.get_init():
                pygame.mixer.quit()
                if self.verbose: logging.info("Pygame mixer quit successfully.")
