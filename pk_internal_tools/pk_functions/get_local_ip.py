def get_local_ip():
    import socket
    # 로컬 IP 얻기 (localhost 제외)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))  # 외부와 연결을 시도
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = 'localhost'
    finally:
        s.close()
    return local_ip
