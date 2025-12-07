@echo off
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\ElevateScript.vbs"
echo UAC.ShellExecute "cmd.exe", "/c ""%~1""", "", "runas", 1 >> "%temp%\ElevateScript.vbs"
cscript //nologo "%temp%\ElevateScript.vbs"
del "%temp%\ElevateScript.vbs"
