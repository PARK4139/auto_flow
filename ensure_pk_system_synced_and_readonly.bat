@echo off
chcp 65001 > nul
setlocal

REM ============================================================================
REM ensure_pk_system_synced_and_readonly.bat
REM ============================================================================
REM
REM This script syncs Python dependencies using 'uv' and then sets the installed
REM package files to be read-only at the file-system level.
REM
REM
REM [WHY THIS SCRIPT IS NEEDED]
REM
REM 1. Problem: Standard Python package installers (like pip or uv) do not
REM    have a built-in feature to set file-system read-only attributes after
REM    installation. Their job is simply to place the package files in the
REM    'site-packages' directory.
REM
REM 2. Goal: For this project, we want to explicitly mark library files as
REM    read-only. This prevents accidental edits from within an IDE, as many
REM    IDEs will visually indicate that the file is read-only or lock it.
REM    This helps maintain the integrity of the project's dependencies.
REM
REM 3. Solution: This script automates the required two-step process:
REM    Step 1: Sync dependencies using 'uv'. The --no-cache flag is used to
REM            ensure the latest version is fetched from the git repository.
REM    Step 2: Apply the read-only attribute (+R) to the installed files
REM            using the 'attrib' command.
REM
REM ============================================================================


echo [1/3] Syncing dependencies with uv (using --no-cache)...

REM Check if uv is installed, if not, install it.
if not exist ".\.venv\Scripts\uv.exe" (
    echo uv not found in the current virtual environment. Attempting to install uv via pip...
    ".\.venv\Scripts\python.exe" -m pip install uv
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Failed to install uv via pip. Please ensure pip is working correctly in the virtual environment. Aborting script.
        exit /b %errorlevel%
    )
    echo uv installed successfully.
)

uv pip sync pyproject.toml --no-cache

REM Check the exit code of the last command. %errorlevel% holds it.
if %errorlevel% neq 0 (
    echo.
    echo ERROR: 'uv pip sync --no-cache' failed. Aborting script.
    exit /b %errorlevel%
)

echo.
echo [2/3] Setting read-only attribute for 'pk_system' package files...

REM The 'pk_system' package should now be installed correctly under a single
REM 'pk_system' directory in site-packages.
set SITEPACKAGES_PATH=.venv\Lib\site-packages
attrib +R "%SITEPACKAGES_PATH%\pk_system\*.*" /S > nul

echo.
echo [3/3] Task complete. Dependencies are synced and set to read-only.
echo.

endlocal
