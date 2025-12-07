def get_random_int(max=100):
    import secrets
    return secrets.randbelow(max)  # 0부터 99까지의 난수 생성
