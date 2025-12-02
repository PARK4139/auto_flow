@echo on
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion

rem === Config (edit only this line) ========================================
set "FILENAME=LM-100 Spindle 내구성 시험이력(박정훈).xlsx"
rem ========================================================================
rem --- Derived values (do not edit) ---------------------------------------
set "SCRIPT_DIR=%~dp0"
set "SRC_FILE=%SCRIPT_DIR%%FILENAME%"
for %%F in ("%FILENAME%") do set "BASE_NAME=%%~nF"
set "ARCHIVED_DIR=%SCRIPT_DIR%archived"
set "PS=PowerShell -NoProfile -ExecutionPolicy Bypass -Command"
rem ------------------------------------------------------------------------

echo [STEP] Verifying source file exists...
if not exist "%SRC_FILE%" (
  echo [ERROR] Source not found: "%SRC_FILE%"
  goto :END_FAIL
)

echo [STEP] Making timestamp (yyyyMMdd HHmm)...
for /f "usebackq delims=" %%T in (`%PS% "$d=Get-Date; $d.ToString('yyyyMMdd HHmm')"`) do set "TS=%%T"
if not defined TS (
  echo [ERROR] Failed to generate timestamp via PowerShell.
  goto :END_FAIL
)
echo [OK] TS = "%TS%"

set "DEST_NAME=%BASE_NAME% - %TS%.xlsx"
set "DEST_PATH=%SCRIPT_DIR%%DEST_NAME%"

echo [STEP] Copy -> "%DEST_NAME%" ...
copy /Y /V "%SRC_FILE%" "%DEST_PATH%"
if errorlevel 1 (
  echo [ERROR] Copy failed to "%DEST_PATH%"
  goto :END_FAIL
)

echo [STEP] Ensure archived dir exists...
if not exist "%ARCHIVED_DIR%" (
  mkdir "%ARCHIVED_DIR%"
  if errorlevel 1 (
    echo [ERROR] Failed to create archived dir: "%ARCHIVED_DIR%"
    goto :END_FAIL
  )
)

echo [STEP] Move -> archived\ ...
move /Y "%DEST_PATH%" "%ARCHIVED_DIR%\" >nul
if errorlevel 1 (
  echo [ERROR] Move failed into "%ARCHIVED_DIR%"
  goto :END_FAIL
)

echo [SUCCESS] Archived: "%ARCHIVED_DIR%\%DEST_NAME%"
goto :END_OK

:END_FAIL
echo.
echo ===== FAILED =====
echo (Hint) If Korean file names/paths are garbled, save this file as UTF-8 (no BOM).
goto :END_COMMON

:END_OK
echo.
echo ===== DONE =====

:END_COMMON
echo.
endlocal
exit /b
