uv pip uninstall pywin32
uv pip install pypiwin32

@REM pypiwin32 is pywin32 wrapping pkg




@REM [today python error]
@REM "~~~~ .venv\Lib\site-packages\prompt_toolkit\output\win32.py", line 219, in get_win32_screen_buffer_info
@REM     raise NoConsoleScreenBufferError
@REM prompt_toolkit.output.win32.NoConsoleScreenBufferError: No Windows console found. Are you running cmd.exe?
@REM [solution]
@REM Emulate terminal in output console 체크 안되어 있어서 체크 했더니 solved   