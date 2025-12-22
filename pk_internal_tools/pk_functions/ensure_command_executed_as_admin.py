def ensure_command_executed_as_admin(cmd):
    import textwrap

    from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
    from pk_internal_tools.pk_objects.pk_encodings import PkEncoding

    import platform
    import importlib

    import os
    if platform.system() == 'Windows':
        subprocess = importlib.import_module("subprocess")

        os.system(rf'chcp 65001')

        file = rf"{D_PK_EXTERNAL_TOOLS}\elevate_cmd.cmd"
        # pk_* -> 배치파일 생성
        script = textwrap.dedent(rf'''
                @echo off
                echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\ElevateScript.vbs"
                echo UAC.ShellExecute "cmd.exe", "/c ""%~1""", "", "runas", 1 >> "%temp%\ElevateScript.vbs"
                cscript //nologo "%temp%\ElevateScript.vbs"
                del "%temp%\ElevateScript.vbs"
                ''').lstrip()
        with open(file, 'w', encoding='utf-8') as f:
            f.write(script)

        # 배치파일 실행
        admin_cmd = f'cmd /c {file} "{cmd}"'
        result = subprocess.run(admin_cmd, shell=True, encoding=PkEncoding.UTF8.value, errors="replace", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode, result.stdout, result.stderr
