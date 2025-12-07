import logging
from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

ensure_pk_log_initialized(__file__)

@ensure_seconds_measured
def get_text_decoded(text: str, master_password: str):
    """
    텍스트 복호화 함수
    1. 마스터 패스워드로 메타데이터 복호화
    2. 다단계 복호화 수행 (Base64 + AES + XOR + Caesar Cipher)
    3. return decoded text
    """
    logging.debug(f"get_text_decoded 함수 호출됨. text 길이: {len(text)}, master_password 길이: {len(master_password)}")
    from base64 import b64decode
    from Cryptodome.Cipher import AES
    import hashlib
    import json

    # 키 파생 함수
    def derive_key_from_password(password, salt):
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    # 메타데이터 복호화 함수
    def decrypt_metadata(encrypted_metadata, password):
        try:
            # Salt 추출 (처음 16바이트)
            salt = encrypted_metadata[:16]
            encrypted_data = encrypted_metadata[16:]
            logging.debug(f"decrypt_metadata: Salt 길이: {len(salt)}, 암호화된 데이터 길이: {len(encrypted_data)}")

            key = derive_key_from_password(password, salt)
            logging.debug(f"decrypt_metadata: 파생된 키 길이: {len(key)}")
            cipher = AES.new(key, AES.MODE_ECB)

            decrypted = cipher.decrypt(encrypted_data)
            logging.debug(f"decrypt_metadata: AES 복호화 완료. 결과 길이: {len(decrypted)}")
            # null 패딩 제거
            metadata_json = decrypted.rstrip(b'\0').decode('utf-8')
            logging.debug(f"decrypt_metadata: UTF-8 디코딩 완료. JSON 문자열: {metadata_json[:100]}...") # Log first 100 chars
            return json.loads(metadata_json)
        except Exception as e:
            logging.error(f"decrypt_metadata: 메타데이터 복호화 중 오류 발생: {e}", exc_info=True)
            return None

    # 보안 형식 확인
    if not text.startswith("SECURE_"):
        logging.debug("텍스트가 'SECURE_'로 시작하지 않아 복호화 실패.")
        return None

    # 데이터 분리
    parts = text.split("_", 2)
    if len(parts) != 3:
        logging.debug(f"텍스트 분리 실패. 예상치 못한 파트 수: {len(parts)}")
        return None

    encrypted_metadata_b64 = parts[1]
    encrypted_data = parts[2]
    logging.debug(f"메타데이터 Base64 인코딩 길이: {len(encrypted_metadata_b64)}, 암호화된 데이터 길이: {len(encrypted_data)}")

    # 메타데이터 복호화
    encrypted_metadata = b64decode(encrypted_metadata_b64)
    logging.debug(f"Base64 디코딩된 메타데이터 길이: {len(encrypted_metadata)}")
    metadata = decrypt_metadata(encrypted_metadata, master_password)

    if metadata is None:
        logging.debug("메타데이터 복호화 실패.")
        return None
    logging.debug(f"메타데이터 복호화 성공: {metadata}")

    caesar_shift = metadata['caesar_shift']
    xor_key = metadata['xor_key']
    aes_key = metadata['aes_key']
    logging.debug(f"추출된 메타데이터: caesar_shift={caesar_shift}, xor_key={xor_key}, aes_key={aes_key}")

    # 단계 1: Base64 디코딩
    def base64_decode(text):
        return b64decode(text)

    # 단계 2: AES 복호화
    def aes_decrypt(encrypted_data, key):
        key_hash = hashlib.sha256(key.encode()).digest()
        cipher = AES.new(key_hash, AES.MODE_ECB)
        decrypted = cipher.decrypt(encrypted_data)
        # null 패딩 제거
        return decrypted.rstrip(b'\0').decode('utf-8')

    # 단계 3: XOR 복호화
    def xor_decrypt(text, key):
        key_bytes = key.encode('utf-8')
        result = ""
        for i, char in enumerate(text):
            result += chr(ord(char) ^ key_bytes[i % len(key_bytes)])
        return result

    # 단계 4: Caesar Cipher 복호화
    def caesar_decrypt(text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            else:
                result += char
        return result

    # 복호화 과정
    # 1단계: Base64 디코딩
    step1 = base64_decode(encrypted_data)
    logging.debug(f"1단계 (Base64 디코딩) 완료. 결과 길이: {len(step1)}")

    # 2단계: AES 복호화
    step2 = aes_decrypt(step1, aes_key)
    logging.debug(f"2단계 (AES 복호화) 완료. 결과 길이: {len(step2)}")

    # 3단계: XOR 복호화
    step3 = xor_decrypt(step2, xor_key)
    logging.debug(f"3단계 (XOR 복호화) 완료. 결과 길이: {len(step3)}")

    # 4단계: Caesar Cipher 복호화
    plain__decoded = caesar_decrypt(step3, caesar_shift)
    logging.debug(f"4단계 (Caesar Cipher 복호화) 완료. 최종 결과 길이: {len(plain__decoded)}")

    logging.debug("get_text_decoded 함수 종료.")
    return plain__decoded
