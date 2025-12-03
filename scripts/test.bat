@echo off
title AutoFlow Test Runner
echo.
echo ===============================
echo  AutoFlow Test Suite
echo ===============================
echo.

REM Execute the main test script using the system's python.
REM test.py will handle environment setup and call pytest.
python scripts/test.py

set /A TEST_EXIT_CODE=%ERRORLEVEL%

echo.
echo ===============================
if %TEST_EXIT_CODE% == 0 (
    echo  All tests passed successfully!
) else (
    echo  Some tests failed. Check the output above.
)
echo ===============================
echo.

pause
exit /b %TEST_EXIT_CODE%
