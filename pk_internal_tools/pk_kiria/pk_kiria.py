import logging
import threading
import time
import traceback
from typing import Optional, Callable

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
# Lazy import for ensure_pk_system_log_initialized
from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE

# Initialize logging for this module
ensure_pk_system_log_initialized(__file__)
logger = logging.getLogger(__name__)

# Import newly structured Kiria components
from pk_internal_tools.pk_kiria.pk_stt_engine import PkSTTModel
from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken, get_pk_spoken_manager
from pk_internal_tools.pk_kiria.pk_text_cleaner import KoreanCleaner
from pk_internal_tools.pk_kiria.pk_audio_io import AudioInput
from pk_internal_tools.pk_kiria.pk_voice_pipeline import VoicePipeline, VoiceWorkflowBase


class PkKiriaWorkflow(VoiceWorkflowBase):
    """
    PkKiria's specific workflow for processing voice commands.
    This is where the actual logic for responding to commands resides.
    """

    def __init__(self, ensure_spoken_func: Callable):
        self.ensure_spoken_func = ensure_spoken_func
        logger.info("PkKiriaWorkflow initialized.")

    def process_command(self, command: str) -> Optional[str]:
        logger.info(f"PkKiriaWorkflow processing command: '{command}'")
        response: Optional[str] = None

        # Example command processing logic
        if "안녕" in command or "하이" in command:
            response = "안녕하세요, 무엇을 도와드릴까요?"
        elif "시간" in command:
            response = f"현재 시간은 {time.strftime('%H시 %M분')}입니다."
        elif "날씨" in command:
            response = "아직 날씨 정보를 가져오는 기능은 구현되지 않았습니다."
        elif "바이브 코딩 모드" in command:
            response = "아직 준비 되지 않은 서비스입니다."
        # "그만" or "종료" are now handled by the pipeline to switch to SLEEPING mode.
        else:
            response = f"죄송합니다. '{command}' 명령을 이해하지 못했습니다. 더 많은 기능을 학습 중입니다."

        logger.info(f"PkKiriaWorkflow response: '{response}'")
        return response


class PkKiria:
    """
    Main class for the PkKiria voice assistant.
    Integrates all components to provide voice-based interaction.
    """

    def __init__(self):
        self.stt_model = PkSTTModel(language_code="ko-KR")
        self.tts_engine = get_pk_spoken_manager()  # Use the global PkSpokenManager instance
        self.text_cleaner = KoreanCleaner()
        self.workflow = PkKiriaWorkflow(ensure_spoken_func=ensure_spoken)
        # The new VoicePipeline handles state management internally.
        self.voice_pipeline = VoicePipeline(
            stt_model=self.stt_model,
            tts_engine=self.tts_engine,
            text_cleaner=self.text_cleaner,
            audio_input_class=AudioInput,
            workflow=self.workflow
            # wake_word and inactivity_timeout use default values
        )
        self.stop_event = threading.Event()
        self.running_thread: Optional[threading.Thread] = None
        logger.info("PkKiria voice assistant initialized.")

    def start_listening(self):
        """Starts PkKiria in continuous listening mode."""
        if self.running_thread and self.running_thread.is_alive():
            logger.warning("PkKiria is already listening.")
            return

        logger.info(PK_UNDERLINE)
        logger.info(f"{PkColors.BRIGHT_CYAN}PkKiria: 음성 비서 듣기 시작{PkColors.RESET}")
        logger.info(PK_UNDERLINE)

        self.stop_event.clear()
        self.running_thread = threading.Thread(target=self._run_pipeline_continuously, daemon=True)
        self.running_thread.start()
        # Announce start-up; the pipeline handles prompts from here.
        ensure_spoken("Kiria, 대기 모드로 시작합니다.", read_finished_wait_mode=True)
        logger.info("PkKiria listening thread started.")

    def _run_pipeline_continuously(self):
        """Internal method to run the voice pipeline continuously."""
        self.voice_pipeline.run_continuously(self.stop_event)
        logger.info("PkKiria continuous pipeline stopped.")

    def stop_listening(self):
        """Stops PkKiria from listening."""
        if not (self.running_thread and self.running_thread.is_alive()):
            logger.warning("PkKiria is not currently listening.")
            return

        self.stop_event.set()
        if self.running_thread:
            self.running_thread.join(timeout=5)  # Wait for thread to finish
            if self.running_thread.is_alive():
                logger.error("PkKiria listening thread did not terminate gracefully.")
        ensure_spoken("Kiria를 종료합니다.", read_finished_wait_mode=True)
        logger.info("PkKiria listening stopped.")

    def run_single_command(self):
        """Runs PkKiria for a single voice command cycle."""
        logger.info(PK_UNDERLINE)
        logger.info(f"{PkColors.BRIGHT_CYAN}PkKiria: 단일 명령 처리 시작{PkColors.RESET}")
        logger.info(PK_UNDERLINE)
        self.voice_pipeline.run_one_cycle()
        logger.info("PkKiria single command cycle finished.")

    def terminate(self):
        """Terminates PkKiria, stopping all background processes."""
        self.stop_listening()
        self.tts_engine.terminate()
        logger.info("PkKiria terminated.")


def ensure_pk_kiria_executed_continuously():
    """
    PkKiria 음성 비서를 지속적으로 실행합니다.
    """
    try:
        pk_kiria = PkKiria()
        pk_kiria.start_listening()
        # Keep the main thread alive for the daemon thread
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt detected. Stopping PkKiria.")
        finally:
            pk_kiria.stop_listening()
            pk_kiria.terminate()
            logger.info("PkKiria gracefully stopped.")
        return True
    except Exception as e:
        logger.error(f"PkKiria continuous execution failed: {e}", exc_info=True)
        ensure_debugged_verbose(traceback, e)
        return False


def ensure_pk_kiria_executed_single_command():
    """
    PkKiria 음성 비서를 단일 명령 처리 모드로 실행합니다.
    """
    try:
        pk_kiria = PkKiria()
        pk_kiria.run_single_command()
        pk_kiria.terminate()
        return True
    except Exception as e:
        logger.error(f"PkKiria single command execution failed: {e}", exc_info=True)
        ensure_debugged_verbose(traceback, e)
        return False
