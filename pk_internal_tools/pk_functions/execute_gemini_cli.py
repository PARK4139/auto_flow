import subprocess
import json
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_gemini_cli_message import GeminiCliMessage

@ensure_seconds_measured
def execute_gemini_cli(prompt: str, input_text: str = None) -> GeminiCliMessage:
    """
    Executes the Gemini CLI with a given prompt and optional input text.

    Args:
        prompt (str): The prompt to send to Gemini.
        input_text (str, optional): Text to pipe to Gemini's stdin. Defaults to None.

    Returns:
        GeminiCliMessage: An object containing the response and status.
    """
    try:
        # If there is input_text, we pipe it to the gemini command within PowerShell
        if input_text:
            powershell_command = f'$Input | gemini -p "{prompt}" --output-format json'
        else:
            powershell_command = f'gemini -p "{prompt}" --output-format json'

        process_input = input_text
        
        gemini_process = subprocess.Popen(
            ["powershell.exe", "-NoProfile", "-Command", powershell_command],
            stdin=subprocess.PIPE if process_input else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            shell=False
        )

        stdout, stderr = gemini_process.communicate(input=process_input)



        if gemini_process.returncode != 0:
            error_msg = f"Gemini process failed with error: {stderr}"
            from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
            ensure_debug_loged_verbose(error_msg)
            return GeminiCliMessage(prompt=prompt, status="error", error_message=error_msg)

        try:
            json_start = stdout.find('{')
            if json_start == -1:
                error_msg = f"No JSON object found in Gemini output: {stdout}"
                from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
                ensure_debug_loged_verbose(error_msg)
                return GeminiCliMessage(prompt=prompt, status="error", error_message=error_msg)
            
            json_response = json.loads(stdout[json_start:])
            message = json_response.get('response', '')
            return GeminiCliMessage(prompt=prompt, response=message, status="success")
        except json.JSONDecodeError as e:
            error_msg = f"Failed to decode JSON: {e}\nOutput was: {stdout}"
            from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
            ensure_debug_loged_verbose(error_msg)
            return GeminiCliMessage(prompt=prompt, status="error", error_message=error_msg)

    except FileNotFoundError:
        error_msg = "powershell.exe or gemini command not found. Make sure they are in your PATH."
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        ensure_debug_loged_verbose(error_msg)
        return GeminiCliMessage(prompt=prompt, status="error", error_message=error_msg)
    except Exception as e:
        error_msg = str(e)
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        import traceback
        ensure_debug_loged_verbose(traceback)
        return GeminiCliMessage(prompt=prompt, status="error", error_message=error_msg)
