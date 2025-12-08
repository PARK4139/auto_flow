import subprocess
import sys
import os

# Define paths using raw strings for Windows paths
python_exe = r"C:\Users\USER\Desktop\박정훈\auto_flow\.venv\Scripts\python.exe"
target_script = r"C:\Users\USER\Desktop\박정훈\auto_flow\business_logic\wrappers\Huvitz\Huvitz mail 열기.py"

if not os.path.exists(target_script):
    print(f"Error: Target script not found at {target_script}", file=sys.stderr)
    sys.exit(1)

if not os.path.exists(python_exe):
    print(f"Error: Python executable not found at {python_exe}", file=sys.stderr)
    sys.exit(1)

try:
    # Construct the command string with proper quoting for the shell
    command_string = f'"{python_exe}" "{target_script}"'
    print(f"Executing command: {command_string}", file=sys.stderr) # Debugging output

    # Use shell=True and pass the command as a single string
    # This relies on the shell (cmd.exe or powershell.exe) to parse the string
    result = subprocess.run(command_string, check=False, text=True, capture_output=True, shell=True)
    
    if result.stdout:
        print("Stdout:\n", result.stdout)
    if result.stderr:
        print("Stderr:\n", result.stderr)
    
    sys.exit(result.returncode) # Propagate the exit code
except Exception as e:
    print(f"An unexpected error occurred: {e}", file=sys.stderr)
    sys.exit(1)
