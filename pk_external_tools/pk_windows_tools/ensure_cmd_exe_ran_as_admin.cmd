chcp 65001
@echo off
echo Set objShell = CreateObject("Shell.Application") > %temp%\run.vbs
echo objShell.ShellExecute "cmd.exe", "", "", "runas", 1 >> %temp%\run.vbs
%temp%\run.vbs
del %temp%\run.vbs
exit