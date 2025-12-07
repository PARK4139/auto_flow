



from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed


def compress_pnx_via_bz_exe(pnx, f_zip):
    cmd = f'bz.exe c "{f_zip}" "{pnx}"'
    ensure_command_executed(cmd=cmd)
