

def get_random_bytes():
    import secrets
    return secrets.token_bytes(16)  # 16바이트의 보안적으로 안전한 난수 생성
