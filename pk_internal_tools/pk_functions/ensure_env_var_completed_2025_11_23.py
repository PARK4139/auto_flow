from typing import Optional

from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.ensure_pk_env_file_setup import ensure_pk_env_file_setup
from pk_internal_tools.pk_functions.ensure_sensitive_info_masked import ensure_sensitive_info_masked

env_path = ensure_pk_env_file_setup()


def ensure_env_var_completed_2025_11_23(
        env_var_name: str,  # TODO : env_var_id 가 필요할수 있음.
        prompt_message: str,
        mask_log: bool = True,
        sensitive_masking_mode=None,
        options=None,
) -> Optional[str]:
    """
    환경 변수에서 값을 가져오거나, 없으면 사용자 입력/옵션 선택을 통해 값을 받습니다.
    선택적으로 .env 파일에 저장하고, 로그에 마스킹 처리할 수 있습니다.
    """
    import logging
    import os

    from dotenv import set_key

    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    env_var_name = env_var_name.upper()

    value = os.getenv(env_var_name)
    default_value = None

    # ---------------------------
    # Case 1. options가 없는 경우
    # ---------------------------
    if options is None:
        if not value:
            logging.warning(f"Environment variable '{env_var_name}' not found.")
            value = input(prompt_message).strip()
            if not value:
                logging.error(
                    f"Input for '{env_var_name}' cannot be empty. Using default fallback if available."
                )
                value = default_value

            # Optional: Ask to save to .env
            if value and value != default_value:
                save_to_env = (
                    input(
                        f"Do you want to save '{env_var_name}' to your .env file for future use? (y/n): "
                    )
                    .strip()
                    .lower()
                )
                if save_to_env == "y":
                    try:
                        set_key(env_path, env_var_name, value)
                        logging.info(f"'{env_var_name}' saved to {env_path}")
                    except Exception as e:
                        logging.error(
                            f"Failed to save '{env_var_name}' to .env file: {e}"
                        )

        # Final fallback
        if not value:
            value = default_value
            if value:
                logging.warning(f"Using default value for '{env_var_name}': {value}")
            else:
                logging.error(
                    f"No value found for '{env_var_name}' and no default provided."
                )
                return None

    # ---------------------------
    # Case 2. options가 있는 경우
    # ---------------------------
    else:
        if not value:  # ENV에 값이 없을 때만 options에서 선택
            logging.warning(f"Environment variable '{env_var_name}' not found.")
            choice = ensure_value_completed_2025_10_12_0000(key_name=prompt_message, options=options)
            value = choice

            # .env 파일에 저장
            try:
                set_key(env_path, env_var_name, value)
                logging.info(f"'{env_var_name}' saved to {env_path}")
            except Exception as e:
                logging.error(f"Failed to save '{env_var_name}' to .env file: {e}")

    if sensitive_masking_mode is None:
        sensitive_masking_mode = True if QC_MODE else False

    log_value = (ensure_sensitive_info_masked(value) if mask_log and sensitive_masking_mode else value)
    logging.info(f"env var value obtained for '{env_var_name}': {log_value}")
    return value
