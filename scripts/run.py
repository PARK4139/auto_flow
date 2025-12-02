import os
import subprocess
import sys
import stat
from pathlib import Path

def run_command(command, shell=False, check=True, capture_output=True, text=True, encoding='utf-8', **kwargs):
    """Runs a command, prints its output, and handles errors."""
    command_str = ' '.join(str(c) for c in command) if isinstance(command, list) else command
    print(f"--> Running: {command_str}")

    # Using Popen for real-time output
    process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=text, encoding=encoding, **kwargs)
    
    if process.stdout:
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
        process.stdout.close()

    if process.stderr:
        for line in iter(process.stderr.readline, ''):
            print(line, end='', file=sys.stderr)
        process.stderr.close()

    return_code = process.wait()

    if check and return_code != 0:
        print(f"\nCommand failed with exit code {return_code}", file=sys.stderr)
        sys.exit(return_code)
        
    return subprocess.CompletedProcess(command, return_code)


def main():
    """Sets up the project environment: creates a venv, syncs dependencies, and sets permissions."""
    if os.name == 'nt':
        try:
            run_command(['chcp', '65001'], shell=True, check=True)
            print("Changed active code page to 65001 (UTF-8).")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: Failed to set console to UTF-8. Some characters may not display correctly.", file=sys.stderr)

    project_root = Path(__file__).parent.parent.resolve()
    venv_path = project_root / ".venv"
    
    # Change working directory to project root
    os.chdir(project_root)

    print("\n--- Checking for virtual environment ---")
    if not venv_path.exists():
        print(f"Virtual environment not found at '{venv_path}'. Creating one...")
        # This requires 'uv' to be in the system's PATH.
        run_command("uv venv", shell=True)
        print("Virtual environment created successfully.")
    else:
        print("Virtual environment found.")
    print("-" * 38)

    # Define python executable for subsequent commands
    python_exe = venv_path / "Scripts" / "python.exe" if os.name == 'nt' else venv_path / "bin" / "python"

    print("\n--- Syncing dependencies with uv (using --no-cache) ---")
    # This command uses the 'uv' executable, which must be in the PATH.
    # It will automatically find and use the .venv in the current directory.
    run_command("uv pip sync pyproject.toml --no-cache", shell=True)
    print("-" * 54)


    print("\n--- Setting read-only attribute for 'pk_system' package ---")
    try:
        # Ask the venv's python for its site-packages path
        get_site_packages_cmd = [str(python_exe), "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"]
        result = subprocess.run(get_site_packages_cmd, capture_output=True, text=True, check=True)
        site_packages_path = Path(result.stdout.strip())
        pk_system_path = site_packages_path / "pk_system"

        if pk_system_path.exists() and pk_system_path.is_dir():
            count = 0
            for root, dirs, files in os.walk(pk_system_path):
                for name in files:
                    filepath = Path(root) / name
                    try:
                        current_permissions = stat.S_IMODE(filepath.stat().st_mode)
                        # Remove write permission for all users
                        filepath.chmod(current_permissions & ~stat.S_IWRITE)
                        count += 1
                    except Exception as e:
                        print(f"Warning: Could not set {filepath} to read-only. Error: {e}", file=sys.stderr)
            print(f"Set {count} files in 'pk_system' package to read-only.")
        else:
            print(f"Warning: 'pk_system' directory not found at '{pk_system_path}'. Skipping read-only attribute setting.", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred while trying to set read-only attributes: {e}", file=sys.stderr)
    print("-" * 63)

    print("\n--- Task complete ---")
    print("Dependencies are synced and 'pk_system' is set to read-only.")

if __name__ == "__main__":
    main()
