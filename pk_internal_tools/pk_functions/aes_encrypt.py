

def aes_encrypt(key, plaintext):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    """AES 암호화: 대칭키암호화 ECB 모드, 보안취약"""
    # 키 생성
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # 패딩 추가
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # 암호화 수행
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext
