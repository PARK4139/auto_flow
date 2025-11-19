@echo on
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion

rem === Config ===============================================================
set "FILENAME=LM-100 Spindle 내구성 시험이력(박정훈).xlsx"
set "BASE_NAME=LM-100 Spindle 내구성 시험이력(박정훈)"
set "SCRIPT_DIR=%~dp0"
set "SRC_FILE=%SCRIPT_DIR%%FILENAME%"
set "ARCHIVED_DIR=%SCRIPT_DIR%archived"
set "PS=PowerShell -NoProfile -ExecutionPolicy Bypass -Command"
rem ==========================================================================

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

echo [STEP] Move -> archived\
move /Y "%DEST_PATH%" "%ARCHIVED_DIR%\"
if errorlevel 1 (
  echo [ERROR] Move failed into "%ARCHIVED_DIR%"
  goto :END_FAIL
)

echo [SUCCESS] Archived: "%ARCHIVED_DIR%\%DEST_NAME%"
goto :END_OK

:END_FAIL
echo.
echo ===== FAILED =====
echo (힌트) 한글 파일명/경로가 깨지면 이 파일을 UTF-8(BOM 없음)으로 저장했는지 확인하세요.
goto :END_COMMON

:END_OK
echo.
echo ===== DONE =====

:END_COMMON
echo.


@REM CODE FOR DEBUGGING
@REM pause


endlocal