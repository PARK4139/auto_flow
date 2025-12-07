def ensure_chcp_65001():
    import os
    os.system("chcp 65001 >NUL")
