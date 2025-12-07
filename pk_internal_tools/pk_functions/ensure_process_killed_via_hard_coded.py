def ensure_process_killed_via_hard_coded():
    nxs = [
        # "python.exe", # 프로그램 스스로를 종료시켜는 방법
        "alsong.exe",
        "cortana.exe",
        "mysqld.exe",
        "KakaoTalk.exe",
        "OfficeClickToRun.exe",
        "TEWebP.exe",
        "TEWeb64.exe",
        "TEWebP64.exe",
        "AnySign4PC.exe",
    ]
    for nx in nxs:
        ensure_process_killed_via_wmic(process_img_n=nx)
