import subprocess

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.execute_gemini_cli import execute_gemini_cli
from pk_internal_tools.pk_objects.pk_gemini_cli_message import GeminiCliMessage


@ensure_seconds_measured
def get_commit_message() -> GeminiCliMessage:
    """
    Generates a commit message for staged git changes using the Gemini CLI.

    This function gets the diff of staged files and passes it to the
    `execute_gemini_cli` function to generate a commit message.

    Returns:
        GeminiCliMessage: An object containing the generated commit message and status.
    """
    try:
        git_diff_process = subprocess.Popen(
            ["git", "diff", "--cached"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        stdout, stderr = git_diff_process.communicate()

        if git_diff_process.returncode != 0:
            error_msg = f"git diff --cached failed with error: {stderr}"
            from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
            ensure_debug_loged_verbose(error_msg)
            return GeminiCliMessage(prompt=None, status="error", error_message=error_msg)

        if not stdout:
            return GeminiCliMessage(prompt=None, response="No changes to commit.", status="success")

        prompt = "Write a concise commit message for these changes"
        return execute_gemini_cli(prompt=prompt, input_text=stdout)

    except FileNotFoundError:
        error_msg = "git command not found. Make sure it is in your PATH."
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        ensure_debug_loged_verbose(error_msg)
        return GeminiCliMessage(prompt=None, status="error", error_message=error_msg)
    except Exception as e:
        error_msg = str(e)
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        import traceback
        ensure_debug_loged_verbose(traceback)
        return GeminiCliMessage(prompt=None, status="error", error_message=error_msg)
