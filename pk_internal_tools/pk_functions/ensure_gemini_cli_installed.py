from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_installed(installed):
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
    from pk_internal_tools.pk_functions.get_gemini_installer_title import get_gemini_installer_title

    from pk_internal_tools.pk_functions.is_gemini_installed import is_gemini_installed
    from pk_internal_tools.pk_functions.ensure_command_executed_like_human import (
        ensure_command_executed_like_human,
    )
    from pk_internal_tools.pk_functions.ensure_script_file_created import (
        ensure_script_file_created,
    )
    from pk_internal_tools.pk_objects.pk_files import F_TEMP_PS1

    import textwrap

    gemini_installer_title = get_gemini_installer_title()
    ensure_window_title_replaced(gemini_installer_title)

    if installed is None:
        installed = is_gemini_installed()

    if not installed:
        script_to_install = """
            Write-Host "Gemini CLI not found. Installing latest..."
            npm install -g @google/gemini-cli
        """
    else:
        ensure_spoken(f'gemini 최신 버전이 나왔습니다. 최신버전으로 자동 업데이트를 시작합니다')
        script_to_install = """
            try {
              $current = (gemini --version) -replace '[^0-9.]',''
              $latest  = (npm show @google/gemini-cli version) -replace '[^0-9.]',''
              if ($current -and $latest) {
                Write-Host "Current Gemini CLI version = $current"
                Write-Host "Latest Gemini CLI version  = $latest"
                if ([version]$current -lt [version]$latest) {
                  Write-Host "Updating Gemini CLI..."
                  npm install -g @google/gemini-cli
                } else {
                  Write-Host "Gemini CLI is up-to-date."
                }
              } else {
                Write-Host "Unable to check versions. Reinstalling just in case..."
                npm install -g @google/gemini-cli
              }
            } catch {
              Write-Host "Version check failed. Installing latest..."
              npm install -g @google/gemini-cli
            }
        """
    script_content = textwrap.dedent(f'''
        # (A) Ensure Node and npm are available
        node -v
        npm -v

        # (B) Resolve npm global prefix/bin and ensure it's on PATH (User scope)
        $prefix = (npm config get prefix).Trim()
        if (-not $prefix) {{ throw "npm prefix not found. Is Node/npm installed?" }}

        $u = [Environment]::GetEnvironmentVariable("Path","User")
        if ($u -notlike "*$prefix*") {{
          [Environment]::SetEnvironmentVariable("Path", ($u.TrimEnd(';') + ";" + $prefix), "User")
        }}
        if ($env:Path -notlike "*$prefix*") {{ $env:Path += ";" + $prefix }}

        # (C) Install or Update Gemini CLI
        {script_to_install}

        # (D) Verify
        Get-Command gemini -ErrorAction Stop
        gemini --version
    ''').lstrip()

    ensure_script_file_created(script_file=F_TEMP_PS1, script_content=script_content)
    ensure_command_executed_like_human(
        f'start "" powershell -NoExit -ExecutionPolicy Bypass -File "{F_TEMP_PS1}" && exit',
    )
