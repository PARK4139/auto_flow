






def get_pnx_windows_style_v1(pnx):
    pnx = pnx.replace(rf"//", f"/")
    pnx = pnx.replace(rf"/", f"\\")
    pnx = pnx.replace(rf"/mnt/c/", f"C:/")
    pnx = pnx.replace(rf"/mnt/d/", f"D:/")
    pnx = pnx.replace(rf"/mnt/e/", f"E:/")
    pnx = pnx.replace(rf"/mnt/f/", f"F:/")
    return pnx
