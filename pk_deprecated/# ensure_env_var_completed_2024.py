import logging
import os
from typing import Optional

from dotenv import load_dotenv, set_key

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

# Load environment variables from .env file
load_dotenv()


def _ensure_sensitive_info_masked(info: str, visible_chars: int = 4) -> str:
    if not info:
        return ""
    if len(info) <= visible_chars * 2:
        return "*" * len(info)
    return info[:visible_chars] + "*" * (len(info) - visible_chars * 2) + info[len(info) - visible_chars:]


def ensure_env_var_completed_2024(
        env_var_name: str,
        prompt_message: str,
        mask_log: bool = True,
        sensitive_masking_mode=None,
) -> Optional[str]:
    """
    환경 변수에서 값을 가져오거나, 없으면 사용자 입력을 통해 값을 받습니다.
    선택적으로 .env 파일에 저장하고, 로그에 마스킹 처리할 수 있습니다.

    Args:
        env_var_name: 가져올 환경 변수의 이름 (예: "P110M_MATTER_COMMISSION_CODE").
        prompt_message: 사용자에게 값을 요청할 때 표시할 메시지.
        default_value: 환경 변수도 없고 사용자 입력도 없을 경우 사용할 기본값.
                       None이면 값이 없을 경우 None을 반환합니다.
        mask_log: 로그에 값을 마스킹 처리할지 여부. 민감 정보에 사용.

    Returns:
        가져온 값 (str) 또는 값을 얻을 수 없는 경우 None.
    """
    value = os.getenv(env_var_name)

    default_value = None

    if not value:
        logging.warning(f"Environment variable '{env_var_name}' not found.")
        value = input(prompt_message).strip()
        if not value:
            logging.error(f"Input for '{env_var_name}' cannot be empty. Using default fallback if available.")
            value = default_value  # Use default_value if input is empty

        # Optional: Ask to save to .env
        if value and value != default_value:  # Only ask to save if a new value was provided and it's not the default
            save_to_env = input(f"Do you want to save '{env_var_name}' to your .env file for future use? (y/n): ").strip().lower()
            if save_to_env == 'y':
                try:
                    # Determine project root dynamically
                    # This function will be in pk_external_tools/pk_functions/
                    # So project root is 3 levels up
                    current_file_dir = os.path.dirname(os.path.abspath(__file__))
                    project_root = os.path.abspath(os.path.join(current_file_dir, '..', '..', '..'))  # TODO : TODO 지금상태로 둘지. SENSITIVE 로 옮길지 고민이 필요하다.
                    env_path = os.path.join(project_root, '.env')
                    set_key(env_path, env_var_name, value)
                    logging.info(f"'{env_var_name}' saved to {env_path}")
                except Exception as e:
                    logging.error(f"Failed to save '{env_var_name}' to .env file: {e}")

    # Final fallback if still empty
    if not value:
        value = default_value
        if value:
            logging.warning(f"Using default value for '{env_var_name}': {value}")
        else:
            logging.error(f"No value found for '{env_var_name}' and no default provided.")
            return None  # Return None if no value can be obtained
    log_value = None

    if sensitive_masking_mode is None:
        if QC_MODE:
            sensitive_masking_mode = True
        else:
            sensitive_masking_mode = False

    if sensitive_masking_mode == True:
        log_value = _ensure_sensitive_info_masked(value) if mask_log else value
    else:
        log_value = value if mask_log else value
    logging.info(f"env var value obtained for '{env_var_name}': {log_value}")
    return value
