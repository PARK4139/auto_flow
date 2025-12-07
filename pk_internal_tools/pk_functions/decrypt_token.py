

def decrypt_token(ciphertext, iv, key):
    from base64 import b64decode
    from Cryptodome.Cipher import AES
    def unpad(s):
        return s[:-ord(s[-1])]

    cipher = AES.new(key, AES.MODE_CBC, iv=b64decode(iv))
    decrypted = cipher.decrypt(b64decode(ciphertext))
    return unpad(decrypted.decode('utf-8'))
