import logging
from typing import Optional

# Lazy import for project-specific functions and logging
from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

# Initialize logging for this module
ensure_pk_system_log_initialized(__file__)
logger = logging.getLogger(__name__)

# Import AudioInput from the newly created module
# This is kept for type hinting in the method signature, but the mock won't use it.
from pk_internal_tools.pk_kiria.pk_audio_io import AudioInput


class PkSTTModel:
    """
    MOCK STT Model.
    Provides a mock implementation of the Speech-to-Text functionality for local testing.
    Instead of transcribing real audio, it prompts the developer to select a command
    from a predefined list using an fzf-based interface.
    """

    def __init__(self, language_code: str = "ko-KR"):
        """
        Initializes the Mock STTModel.
        """
        self.language_code = language_code
        self.mock_commands = [
            "키리아",
            "안녕",
            "시간",
            "날씨",
            "바이브 코딩 모드",
            "자라",
            "자자",
            "그만",
            "종료",
            # Add other common test commands here
        ]
        logger.info(f"Mock STTModel initialized with language_code: {self.language_code}. "
                    "This engine does not use Google Cloud. It provides a manual prompt for testing.")

    def recognize_stream(self, audio_input: AudioInput) -> Optional[str]:
        """
        Simulates speech recognition by prompting the developer to choose a command.

        Args:
            audio_input: This parameter is ignored by the mock implementation.

        Returns:
            The command string selected by the developer, or None if nothing is selected.
        """
        logger.info("Simulating speech recognition stream...")

        # Use the project's fzf wrapper to get input from the developer
        func_n = get_caller_name()
        selected_command = ensure_value_completed(
            key_name="mock_stt_command",
            func_n=func_n,
            guide_text="[MOCK STT] Kiria가 어떤 말을 들었다고 가정하시겠습니까?",
            options=self.mock_commands,
        )

        if selected_command and selected_command.strip(): # Treat empty strings as no command
            logger.info(f"Simulated Transcript received: '{selected_command}'")
            return selected_command
        else:
            logger.warning("No command selected or an empty command was entered in mock STT prompt.")
            return None
