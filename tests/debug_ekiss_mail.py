import os
import subprocess
import sys
import time
from pathlib import Path

# --- Project Root Setup (similar to other project scripts) ---
try:
    current_file_path = Path(__file__).resolve()
    # Assuming project root is 3 levels up from this script (tests/debug_ekiss_mail.py)
    project_root_path = current_file_path.parents[1]
    if str(project_root_path) not in sys.path:
        sys.path.insert(0, str(project_root_path))
except IndexError:
    print("Error: Could not determine project root. Please check script location.")
    sys.exit(1)

# Import necessary project modules
from pk_internal_tools.pk_objects.pk_files import F_VENV_PYTHON_EXE # Path to venv python executable
from pk_internal_tools.pk_objects.pk_directories import d_pk_logs # Directory for logs
from af_internal_tools.constants.af_directory_paths import D_HUVITS_WRAPPERS_PATH # Path to ekiss mail script


# --- Configuration for .env_test (using dummy values as per discussion) ---
# The user confirmed these are in .env_test, so we will create a temporary .env_test
# with these values for the subprocess.
DUMMY_ENV_VARS = {
    "TEST_EKISS_LOGIN_URL": "https://ekiss.huvitz.com/login.aspx",
    "TEST_EKISS_USER_ID": "250037",
    "TEST_EKISS_PASSWORD": "dummy_password_for_test", # Placeholder, user needs to provide a non-empty one
    "TEST_MAIL_MAIN_URL": "https://ekiss.huvitz.com/main.aspx", # Dummy value
    "TEST_MAIL_WINDOW_URL": "https://ekiss.huvitz.com/mail.aspx", # Dummy value
}

# --- Path to the script to be tested ---
EKISS_MAIL_SCRIPT = D_HUVITS_WRAPPERS_PATH / "ekiss mail 열기.py"

def run_ekiss_mail_script_with_captured_logs():
    print(f"--- Running automated debug test for {EKISS_MAIL_SCRIPT.name} ---")

    # 1. Create a temporary .env_test file with dummy data
    temp_env_path = project_root_path / ".env_test"
    with open(temp_env_path, "w", encoding="utf-8") as f:
        for key, value in DUMMY_ENV_VARS.items():
            f.write(f"{key}='{value}'\n")
    print(f"Created temporary .env_test at: {temp_env_path}")

    # 2. Prepare environment variables for the subprocess
    env = os.environ.copy()
    
    # Ensure project root is in PYTHONPATH for the subprocess
    if 'PYTHONPATH' in env:
        env['PYTHONPATH'] = str(project_root_path) + os.pathsep + env['PYTHONPATH']
    else:
        env['PYTHONPATH'] = str(project_root_path)

    # Set the PK_SUBPROCESS_LOG_FILE for the child process's logging
    timestamp = Path(time.strftime("%Y%m%d_%H%M%S")).name # Shorten timestamp for filename
    subprocess_log_file = d_pk_logs / f"subprocess_{EKISS_MAIL_SCRIPT.name}_{timestamp}_{os.getpid()}.log"
    env['PK_SUBPROCESS_LOG_FILE'] = str(subprocess_log_file)

    print(f"Subprocess logs will be written to: {subprocess_log_file}")
    
    # 3. Launch the subprocess
    command = [str(F_VENV_PYTHON_EXE), str(EKISS_MAIL_SCRIPT)]
    print(f"Executing command: {' '.join(command)}")

    process = subprocess.Popen(
        command,
        env=env, # Pass the modified environment
        stdout=subprocess.PIPE, # Capture stdout
        stderr=subprocess.PIPE, # Capture stderr
        text=True, # Decode stdout/stderr as text
        encoding='cp949', # Explicitly set encoding for Windows console output
    )
    
    # 4. Communicate and wait for process to finish
    stdout, stderr = process.communicate()
    print(f"\n--- Subprocess STDOUT ---\n{stdout}\n--- End Subprocess STDOUT ---")
    print(f"\n--- Subprocess STDERR ---\n{stderr}\n--- End Subprocess STDERR ---")
    print(f"Subprocess exited with code: {process.returncode}")

    # 5. Read and print the subprocess-specific log file
    if subprocess_log_file.exists():
        try:
            with open(subprocess_log_file, 'r', encoding='utf-8') as f:
                subprocess_file_logs = f.read()
            print(f"\n--- Subprocess File Logs from {EKISS_MAIL_SCRIPT.name} ---\n{subprocess_file_logs}\n--- End Subprocess File Logs ---")
        except Exception as e:
            print(f"Error reading subprocess log file {subprocess_log_file}: {e}")
        finally:
            os.remove(subprocess_log_file) # Clean up
            print(f"Cleaned up temporary subprocess log file: {subprocess_log_file}")
    else:
        print(f"Subprocess log file not found: {subprocess_log_file}")

    # 6. Clean up temporary .env_test file
    if temp_env_path.exists():
        os.remove(temp_env_path)
        print(f"Cleaned up temporary .env_test file: {temp_env_path}")

    print(f"--- Automated debug test finished ---")
    return process.returncode

if __name__ == "__main__":
    exit_code = run_ekiss_mail_script_with_captured_logs()
    sys.exit(exit_code)
