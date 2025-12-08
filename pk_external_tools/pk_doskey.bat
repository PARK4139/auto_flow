@echo off
chcp 65001 >NUL

    doskey 1=cd "C:\Users\USER\Downloads"
    doskey 2=cd "C:\Users\USER\Desktop\박정훈\auto_flow"
    doskey 3=cd "C:\Users\USER\Downloads\pk_memo"
    doskey 4=cd "C:\Users\USER\Desktop\박정훈\pk_working"
    doskey 5=cd "C:\Users\USER\Downloads\business_flow"
    doskey 6=cd "C:\Users\USER\Desktop\박정훈\auto_flow\pk_external_tools"
    doskey 7=cd "C:\Users\USER\Desktop\박정훈\auto_flow\pk_external_tools"
    doskey 9=cd "C:\Users\USER\Desktop"
    doskey 0=cd "C:\Users\USER\Desktop\휴지통"
    doskey pk="C:\Users\USER\Desktop\박정훈\auto_flow\.venv\Scripts\python.exe" "C:\Users\USER\Desktop\박정훈\auto_flow\pk_internal_tools\pk_wrappers\pk_ensure_pk_wrapper_starter_executed.py"
    doskey pkt="C:\Users\USER\Desktop\박정훈\auto_flow\.venv\Scripts\python.exe" "C:\Users\USER\Desktop\박정훈\auto_flow\pk_internal_tools\pk_wrappers\pk_ensure_pk_terminal_executed.py"
    doskey pkt="C:\Users\USER\Desktop\박정훈\auto_flow\.venv\Scripts\python.exe" "C:\Users\USER\Desktop\박정훈\auto_flow\pk_internal_tools\pk_wrappers\pk_ensure_pk_terminal_executed.py"
    doskey venv="C:\Users\USER\Desktop\박정훈\auto_flow\.venv\Scripts\activate.bat"
    doskey vscode="C:\Users\USER\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk" $*
    doskey claude="C:\Users\USER\AppData\Local\AnthropicClaude\claude.exe" $*
    doskey pycharm=start "" "C:\Program Files\JetBrains\PyCharm 2025.2.1\bin\pycharm64.exe" $*
    doskey ps=powershell
    doskey psa=powershell -Command "Start-Process powershell -Verb RunAs"
    doskey cmda=start "" "C:\Users\USER\Desktop\박정훈\auto_flow\pk_external_tools\ensure_cmd_exe_ran_as_admin.cmd"
    doskey x=exit
    doskey reboot=shutdown /r /t 0
    doskey poweroff=shutdown /s /t 0
    doskey logout=logoff
    doskey .=explorer.exe .
    doskey ls=dir /b
    doskey cat=type $*
    doskey which=where $*
    doskey pwd=cd $*
    doskey history=doskey /history
    doskey play=explorer.exe $*
    doskey open=explorer.exe $*
    doskey wsld=wsl --distribution Ubuntu
    doskey wsl24=wsl --distribution Ubuntu-24.04
    doskey wsl20=wsl --distribution Ubuntu-20.04
    doskey wsl18=wsl --distribution Ubuntu-18.04
