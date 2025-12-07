chcp 65001
title %~nx0
@echo off
cls

@REM python %~n0.py

:: title %~n0
:: echo %~n0
:: echo %~x0
:: echo %~nx0


color 0a
color df



setlocal
for /f "delims=" %%i in ('Powershell.exe get-date -Format 'yyyy MM dd HH mm ss'') do set yyyymmddhhmmss=%%i
set from=E:\500GB\do\utils\space that test\test_from
set to=E:\500GB\do\utils\space that test\test_to
set python_file=pk_backup_pnxs_as_deprecated.py
pyinstaller --onefile %python_file%
@REM  >nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
@REM  if '%errorlevel%' NEQ '0' ( echo Requesting administrative privileges... goto UACPrompt
@REM  ) else ( goto gotAdmin )
@REM  :UACPrompt
@REM 	 echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
@REM 	 set params = %*:"=""
@REM 	 echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"
@REM 	 "%temp%\getadmin.vbs"
@REM 	 del "%temp%\getadmin.vbs"
@REM 	 exit /B
@REM  :gotAdmin
@REM 	 pushd "%CD%"
@REM 	 CD /D "%~dp0"
@REM  :------------------------------------------ below cript will acted as administrator mode ------------------------------------------

:: CONSOLE SET UP
@REM @echo off >nul
@REM color df >nul
color 0f >nul
@REM color 08 >nul
chcp 65001 >nul
title %~dpnx0 >nul
@REM cls >nul
@REM setlocal >nul 


@REM minimized s
if not "%minimized%"=="" goto :minimized
set minimized=true
start /min cmd /C "%~dpnx0"
goto :EOF
:minimized


:: MAXIMIZED WINDOW 
@REM if not "%maximized%"=="" goto :maximized
@REM set maximized=true
@REM start /max cmd /C "%~dpnx0"
@REM goto :EOF
@REM :maximized







:: RUN PYTHON VIRTUAL ENVIRONMENT
@REM echo "%~dp0venv\Scripts\activate.bat"
call "%~dp0venv\Scripts\activate.bat"
python pk_system.py


:: kill 
wmic process where name="pk_system.exe" delete
taskkill /f /im pk_system.exe
taskkill /f /im python.exe




다운로드
cd %ending_directory%
call curl -O http://%ip%:%port%/%zip_file%

 




@REM 디버깅용 코드
@REM cmd /k