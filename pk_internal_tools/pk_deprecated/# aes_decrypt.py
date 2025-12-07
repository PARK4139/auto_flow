

def aes_decrypt(key, ciphertext):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    """AES 복호화"""
    # 키 생성
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    # 복호화 수행
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # 언패딩
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(decrypted_data) + unpadder.finalize()
    return plaintext
