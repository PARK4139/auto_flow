from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_claude_enabled():
    from pathlib import Path

    from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_objects.pk_files import F_CLAUDE_LNK
    file_exe = Path(F_CLAUDE_LNK)
    ensure_command_executed(cmd=f'start "" "{file_exe}" "{D_PK_ROOT}"')
