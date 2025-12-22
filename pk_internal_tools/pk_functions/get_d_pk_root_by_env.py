from __future__ import annotations

import os
import subprocess
from pathlib import Path


def _get_candidates():
    D_USERPROFILE = Path(os.environ.get('USERPROFILE'))
    return [
        rf"{D_USERPROFILE}\Downloads\pk_system",
        rf"{D_USERPROFILE}\Desktop\pk_system",
    ]


def _print_examples(candidates):
    for root in candidates:
        print(rf"   {root}")


def _copy_first_candidate_to_clipboard(candidates):
    cmd = f'Set-Clipboard -Value "{str(candidates[0])}"'
    subprocess.run(['powershell.exe', '-Command', cmd], check=True)


def _save_environment(key_name, value):
    if Path(value).exists():
        # 세션에 저장
        os.environ[key_name] = value
        print(f"{key_name} is set as environment variable.")

        # 영구저장
        subprocess.run(
            ["powershell.exe", "-Command", f'[Environment]::SetEnvironmentVariable("{key_name}", "{value}", "User")'],
            check=True,
        )
        print(f"{key_name} is saved as *user* environment variable. (You need to reopen terminal)")


def get_d_pk_root_by_env(key_name) -> Path | None:
    """
    Ensure that D_PK_ROOT exists in environment variables.
    If not set, ask user to input the value and set it.
    """
    # Lazy import
    import os

    # 1) Try to get from environment variable
    env_value = os.environ.get(key_name)
    if env_value and env_value.strip():
        return Path(env_value.strip())

    # 2) Ask user to input when not found
    while True:
        print("_" * 55)
        print(f"# INPUT {key_name}")
        print(f"{key_name} is not set as environment variable.")
        print("")
        print(f"examples:")
        candidates = _get_candidates()
        _print_examples(candidates)
        _copy_first_candidate_to_clipboard(candidates)
        print("")
        print(f'first candidate is copied to clipboard.')
        print(f'[WARNING] it can be incorrect pk_system root path')
        print("")
        value = input(f"{key_name}=").strip()
        if not value:
            print("Empty value is not allowed. Please try again.")
            continue
        if not Path(value).exists():
            print(f"Candidate '{value}' does not exist.")
            continue
        _save_environment(key_name=key_name, value=value)
        return Path(value)
