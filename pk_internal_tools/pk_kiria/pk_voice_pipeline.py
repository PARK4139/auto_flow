import logging
import threading
import time
from enum import Enum, auto
from typing import Any, Optional

# Lazy import for ensure_pk_system_log_initialized
from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized

# Initialize logging for this module
ensure_pk_system_log_initialized(__file__)
logger = logging.getLogger(__name__)


class PipelineMode(Enum):
    SLEEPING = auto()
    LISTENING = auto()


class VoiceWorkflowBase:
    """
    Base class for voice-based workflows.
    Defines the interface for processing voice commands.
    """

    def process_command(self, command: str) -> Optional[str]:
        """
        Processes a given voice command.
        Args:
            command: The transcribed text command.
        Returns:
            An optional response string to be spoken back, or None if no response is needed.
        """
        raise NotImplementedError("Subclasses must implement process_command method.")


class VoicePipeline:
    """
    Manages the end-to-end voice processing pipeline:
    Audio Input -> STT -> Command Processing -> TTS -> Audio Output.
    Includes state management for sleep/wake functionality.
    """

    def __init__(self,
                 stt_model: Any,
                 tts_engine: Any,
                 text_cleaner: Any,
                 audio_input_class: Any,
                 workflow: VoiceWorkflowBase,
                 wake_word: str = "키리아",
                 inactivity_timeout: int = 259200):  # 3 days in seconds
        self.stt_model = stt_model
        self.tts_engine = tts_engine
        self.text_cleaner = text_cleaner
        self.audio_input_class = audio_input_class
        self.workflow = workflow
        self.wake_word = wake_word
        self.inactivity_timeout = inactivity_timeout

        self.mode = PipelineMode.SLEEPING
        self.last_interaction_time = 0
        logger.info(f"VoicePipeline initialized. Wake word: '{self.wake_word}', Timeout: {self.inactivity_timeout}s")

    def _listen_for_audio(self, prompt: Optional[str] = None) -> Optional[str]:
        """
        A helper to listen and transcribe.
        If the STT model is a mock, it bypasses audio input and shows a manual prompt.
        Otherwise, it records from the microphone.
        """
        # If we are using the Mock STT, we don't need to access the microphone.
        # We can identify the mock by its class name.
        if self.stt_model.__class__.__name__ == 'STTModel':
            logger.debug("Using Mock STT. Bypassing microphone.")
            if prompt:
                self.tts_engine.speak(prompt)
            # The mock's recognize_stream will show a manual fzf prompt
            return self.stt_model.recognize_stream(None)

        # --- Original logic for real microphone input ---
        transcribed_text: Optional[str] = None
        try:
            with self.audio_input_class() as audio_input:
                audio_input.start_recording()
                if prompt:
                    self.tts_engine.speak(prompt)
                transcribed_text = self.stt_model.recognize_stream(audio_input)
                audio_input.stop_recording()
        except Exception as e:
            logger.error(f"Error during audio listening/transcription: {e}", exc_info=True)
        return transcribed_text

    def _handle_sleeping_state(self):
        """Listens for the wake word."""
        logger.debug("Mode: SLEEPING. Listening for wake word...")
        transcribed_text = self._listen_for_audio()

        if transcribed_text:
            cleaned_text = self.text_cleaner.normalize_text(transcribed_text)
            if self.wake_word in cleaned_text:
                logger.info(f"Wake word '{self.wake_word}' detected.")
                self.mode = PipelineMode.LISTENING
                self.last_interaction_time = time.time()
                self.tts_engine.speak("네, 말씀하세요.")
            else:
                logger.debug(f"Wake word not detected in: '{cleaned_text}'")

    def _handle_listening_state(self):
        """Listens for a command and processes it."""

        from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui

        if time.time() - self.last_interaction_time > self.inactivity_timeout:
            timeout_message = "오랫동안 사용이 없어 Kiria가 대기 모드로 전환됩니다."
            logger.info(f"Inactivity timeout reached. Alerting user: '{timeout_message}'")
            alert_as_gui(timeout_message)
            self.mode = PipelineMode.SLEEPING
            self.tts_engine.speak("다시 대기합니다.")
            return

        logger.debug("Mode: LISTENING. Listening for command...")
        # In LISTENING mode, we don't need to prompt every single time,
        # but it can be helpful if the first command fails.
        # For now, we listen without a repetitive prompt.
        transcribed_text = self._listen_for_audio()

        response_text: Optional[str] = None

        if transcribed_text:
            cleaned_command = self.text_cleaner.normalize_text(transcribed_text)
            logger.info(f"Cleaned command: '{cleaned_command}'")

            # Special handling for commands that change state
            if cleaned_command in ["그만", "잘가", "고마워 이제 그만", "자라", "자자"]:
                logger.info("'Go to sleep' command detected. Switching to SLEEPING mode.")
                self.mode = PipelineMode.SLEEPING
                response_text = "네, 알겠습니다."
            else:
                response_text = self.workflow.process_command(cleaned_command)

            if response_text:
                self.last_interaction_time = time.time()  # Update interaction time only if there's a response
        else:
            logger.warning("No speech recognized in LISTENING mode.")
            # Don't speak anything, just wait for the timeout or next command

        if response_text:
            self.tts_engine.speak(response_text)

    def run_continuously(self, stop_event: threading.Event):
        """
        Runs the voice pipeline continuously with state management until a stop event is set.
        """
        logger.info("Starting stateful continuous voice pipeline operation...")
        self.last_interaction_time = time.time()

        while not stop_event.is_set():
            if self.mode == PipelineMode.SLEEPING:
                self._handle_sleeping_state()
            elif self.mode == PipelineMode.LISTENING:
                self._handle_listening_state()

            time.sleep(0.1)  # Short sleep to prevent busy-waiting

        logger.info("Continuous voice pipeline operation stopped.")

    def run_one_cycle(self) -> Optional[str]:
        """
        Runs a single cycle of the voice pipeline, for single-command mode.
        """
        logger.info("Starting one voice pipeline cycle...")
        transcribed_text: Optional[str] = None
        response_text: Optional[str] = None

        try:
            # In single cycle, always prompt
            transcribed_text = self._listen_for_audio("명령을 말씀해주세요.")

            if transcribed_text:
                cleaned_command = self.text_cleaner.normalize_text(transcribed_text)
                logger.info(f"Cleaned command: '{cleaned_command}'")
                response_text = self.workflow.process_command(cleaned_command)
            else:
                response_text = "죄송합니다. 음성을 인식하지 못했습니다."
                logger.warning("No speech recognized.")

        except Exception as e:
            logger.error(f"Error in voice pipeline cycle: {e}", exc_info=True)
            response_text = "음성 처리 중 오류가 발생했습니다."

        if response_text:
            self.tts_engine.speak(response_text)

        return transcribed_text
