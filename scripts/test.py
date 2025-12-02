import subprocess
import sys
from pathlib import Path
import os

# Ensure project root is in python path to allow sibling imports
_project_root = Path(__file__).parent.parent.resolve()
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Import the main function from run.py to ensure environment is set up
try:
    from scripts.run import main as setup_environment
except ImportError:
    print("Error: scripts/run.py not found. Please ensure it exists.", file=sys.stderr)
    sys.exit(1)

def run_pytest():
    """Runs pytest on the tests/ directory."""
    print("\n--- Running Pytest ---")
    
    # Define path to venv's pytest
    project_root = Path(__file__).parent.parent.resolve()
    venv_path = project_root / ".venv"
    if os.name == 'nt':
        pytest_exe = venv_path / "Scripts" / "pytest.exe"
    else:
        pytest_exe = venv_path / "bin" / "pytest"

    if not pytest_exe.exists():
        print(f"Error: pytest not found at {pytest_exe}", file=sys.stderr)
        print("Please ensure dependencies are installed correctly by running 'python scripts/run.py' first.", file=sys.stderr)
        sys.exit(1)

    # Change to project root to ensure pytest discovers tests correctly
    os.chdir(project_root)
    
    # We pass -v for verbose output.
    command = [str(pytest_exe), "tests/", "-v"]
    
    print(f"--> Executing: {" ".join(command)}")
    print("-" * 25)
    
    # Using check=False to handle test failures gracefully and report them.
    # The output will be streamed directly to the console.
    result = subprocess.run(command)

    print("-" * 25)
    if result.returncode == 0:
        print("✅ All tests passed successfully.")
    else:
        # Pytest non-zero exit codes:
        # 1: Tests failed
        # 2: Interrupted
        # 3: Internal error
        # 4: Usage error
        # 5: No tests collected
        print(f"❌ Pytest finished with exit code {result.returncode} (see details above).", file=sys.stderr)
    
    return result.returncode

def main():
    """Main function to set up environment and run tests."""
    print("=== Test Runner Started ===")
    print("\n[Step 1/2] Setting up project environment...")
    setup_environment()
    print("\n✅ Environment setup complete.")
    
    print("\n[Step 2/2] Running tests...")
    exit_code = run_pytest()
    
    print("\n=== Test Runner Finished ===")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
