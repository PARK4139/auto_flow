

def get_pnx_wsl_unix_style_v1(pnx):
    pnx = pnx.replace(f"\\", rf"/")
    pnx = pnx.replace(f"C:/", rf"/mnt/c/")
    return pnx
