from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_installed_for_one_session(installed):
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
    from pk_internal_tools.pk_functions.get_gemini_installer_title import get_gemini_installer_title

    from pk_internal_tools.pk_functions.is_gemini_installed import is_gemini_installed
    from pk_internal_tools.pk_functions.ensure_command_executed_like_human import \
        ensure_command_executed_like_human
    from pk_internal_tools.pk_functions.ensure_script_file_created import ensure_script_file_created
    from pk_internal_tools.pk_objects.pk_files import F_TEMP_PS1

    import textwrap

    gemini_installer_title = get_gemini_installer_title()
    ensure_window_title_replaced(gemini_installer_title)

    if installed is None:
        installed = is_gemini_installed()

    if not installed:
        script_content = textwrap.dedent('''
                # (A) "Unknown command ..." 섞여버린 PATH 정리 (현재 세션)
                $env:Path = ($env:Path -split ';' | Where-Object { $_ -and ($_ -notmatch '^Unknown command') }) -join ';'
                # (B) 사용자 PATH(영구)에서도 같은 문자열 제거
                $u = [Environment]::GetEnvironmentVariable("Path","User")
                $u = ($u -split ';' | Where-Object { $_ -and ($_ -notmatch '^Unknown command') }) -join ';'
                [Environment]::SetEnvironmentVariable("Path",$u,"User")
                # (C) 올바른 전역 prefix 파악(= 전역 실행 파일 폴더)
                $prefix = (npm config get prefix).Trim()
                Write-Host "npm prefix (global) = $prefix"
                # (D) prefix를 PATH에 추가 (현재 세션 + 영구)
                if ($env:Path -notlike "*$prefix*") { $env:Path += ";$prefix" }
                $u = [Environment]::GetEnvironmentVariable("Path","User")
                if ($u -notlike "*$prefix*") { [Environment]::SetEnvironmentVariable("Path", "$u;$prefix", "User") }
                # (E) 전역에 gemini가 실제로 생겼는지 확인
                Get-ChildItem "$prefix\gemini*" -ErrorAction SilentlyContinue
                npm uninstall -g @google/gemini-cli
                npm install  -g @google/gemini-cli
                Get-Command gemini -All
           ''').lstrip()
        ensure_script_file_created(script_file=F_TEMP_PS1, script_content=script_content)
        ensure_command_executed_like_human(f'start "" powershell -NoExit -ExecutionPolicy Bypass -File "{F_TEMP_PS1}" && exit')
