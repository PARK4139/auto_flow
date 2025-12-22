from __future__ import annotations


def _run_whoami_user() -> str:
    """
    Run `whoami /user` and return stdout as text.
    This helper is intentionally low-level and uses only stdlib.
    """
    import subprocess

    completed = subprocess.run(
        ["whoami", "/user"],
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout


def _extract_sids_from_whoami_output(output: str) -> list[str]:
    """
    Parse SIDs from `whoami /user` output.

    Typical output example:

        USER INFORMATION
        ----------------

        User Name      SID
        ============== ==========================================
        pcname\\user   S-1-5-21-1234567890-2345678901-3456789012-1001

    This function extracts all tokens that look like `S-1-5-...`.
    """
    import re

    sids: list[str] = []

    pattern = re.compile(r"(S-1-5-[0-9\-]+)")

    for line in output.splitlines():
        for match in pattern.findall(line):
            sids.append(match)

    # Deduplicate while preserving order
    seen = set()
    unique_sids: list[str] = []
    for sid in sids:
        if sid not in seen:
            seen.add(sid)
            unique_sids.append(sid)

    return unique_sids


# @ensure_seconds_measured
def get_user_sid(env_key: str = "PK_USER_SID") -> str:
    """
    Lightweight, import-safe function to retrieve the current Windows user SID.

    IMPORTANT:
        - This function MUST NOT import any pk_internal_tools or pk_objects modules.
        - It is used at import-time from pk_objects.pk_directories, so it must
          avoid any circular import risk and any interactive prompts.

    Behavior:
        1. If `env_key` is already set in os.environ, return that value.
        2. Otherwise, run `whoami /user` and parse SIDs from the output.
        3. If multiple SIDs are found, deterministically pick the first one.
        4. Cache the chosen SID into os.environ[env_key] and return it.
    """
    import os

    # 1) Reuse cached value if present
    existing = os.environ.get(env_key)
    if existing:
        return existing

    # 2) Run `whoami /user` to detect SIDs
    raw_output = _run_whoami_user()
    sids = _extract_sids_from_whoami_output(raw_output)
    if not sids:
        raise RuntimeError("No SID found in 'whoami /user' output")

    # 3) If multiple SIDs exist, just choose the first one here.
    #    (Interactive selection is handled in the high-level wrapper.)
    selected_sid = sids[0]

    # 4) Cache in environment for later reuse
    os.environ[env_key] = selected_sid
    return selected_sid


def ensure_user_sid_completed(
    env_key: str = "PK_USER_SID",
    selection_key_name: str = "user_sid_selection",
) -> str | None:
    """
    High-level wrapper that integrates with pk_system helper functions:

    Flow:
        1. Use low-level get_user_sid() to get a base SID and set env_key.
        2. Re-parse `whoami /user` to list all SID candidates.
        3. If multiple candidates exist, let the user pick one via ensure_value_completed().
        4. Use ensure_env_var_completed() so that your existing env-handling mechanism
           can persist/check the final SID value, then return it.

    This function assumes that the following helper functions already exist
    in your codebase (with the given signatures):

        func_n = get_caller_name()

        decision = ensure_value_completed(
            key_name="decision",
            options=["opt1", "opt2"],
            func_n=func_n,
        )

        env_val = ensure_env_var_completed(
            key_name="some_env_key",
            func_n=func_n,
            guide_text="Some description text",
        )

    NOTE:
        - This function SHOULD NOT be used from pk_objects.*
          Call it only from higher-level CLI / wrapper scripts.
    """
    import os

    # Lazy imports: safe here because this function should not be used at import-time
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.ensure_value_completed import (
        ensure_value_completed,
    )
    from pk_internal_tools.pk_functions.ensure_env_var_completed import (
        ensure_env_var_completed,
    )

    func_n = get_caller_name()

    # 1) Start from the low-level core detection
    base_sid = None
    try:
        base_sid = get_user_sid(env_key=env_key)
    except Exception as e:
        # If low-level detection fails, we will fall back to manual input below.
        base_sid = None

    # 2) Collect all candidates from whoami /user (if possible)
    try:
        raw_output = _run_whoami_user()
        sids = _extract_sids_from_whoami_output(raw_output)
    except Exception as e:
        sids = []
        if base_sid:
            sids.append(base_sid)

    # 3) Decide which SID to use
    selected_sid: str | None = None

    if not sids:
        # No SID could be parsed automatically.
        # Fallback: let ensure_env_var_completed handle user input.
        user_sid = ensure_env_var_completed(
            key_name=env_key,
            func_n=func_n,
            guide_text=(
                "현재 Windows 사용자 SID를 입력하세요. "
                "예: whoami /user 명령 결과 중 S-1-5-21-... 형태의 값"
            ),
        )
        if user_sid:
            os.environ[env_key] = user_sid
        return user_sid

    if len(sids) == 1:
        selected_sid = sids[0]
    else:
        # Multiple SIDs detected: let the user choose exactly one.
        selected_sid = ensure_value_completed(
            key_name=selection_key_name,
            options=sids,
            func_n=func_n,
        )

    if selected_sid:
        os.environ[env_key] = selected_sid

    # 4) Delegate to ensure_env_var_completed so your existing mechanism
    #    (e.g. .env file, persistent storage) can handle it uniformly.
    user_sid = ensure_env_var_completed(
        key_name=env_key,
        func_n=func_n,
        guide_text=(
            "현재 Windows 사용자 SID를 확인 또는 수정하세요. "
            "보통 whoami /user 명령 결과 중 S-1-5-21-... 형태의 값입니다."
        ),
    )

    # Sync back (in case user edited the value)
    if user_sid:
        os.environ[env_key] = user_sid
        return user_sid

    # If user did not edit in ensure_env_var_completed, return the selected one
    return selected_sid
