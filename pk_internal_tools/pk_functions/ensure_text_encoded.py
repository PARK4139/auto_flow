def ensure_text_encoded():
    """
    보안 강화 텍스트 암호화 함수
    0. 암호화 복호화 모듈은 실패 케이스 만 로깅
    1. 사용자 입력으로 text와 master_password를 받음
    2. master_password로 메타데이터 암호화
    3. 다단계 암호화 수행 (AES + Base64 + XOR + Caesar Cipher)
    4. print encoded text
    5. 클립보드에 복사
    6. return encoded text
    """
    import logging
    from base64 import b64encode, b64decode
    from Cryptodome.Cipher import AES
    from Cryptodome.Random import get_random_bytes
    import secrets
    import hashlib
    import pyperclip
    import json
    import os

    text = input("plain text(text to encode)=").strip()
    
    if not text:
        logging.debug("텍스트가 입력되지 않았습니다.")
        return None
    
    master_password = input("master_password(5th sym pw)=").strip()
    
    if not master_password:
        logging.debug("master_password가 입력되지 않았습니다.")
        return None
    
    # n. 다단계 암호화 수행
    try:
        # 키 파생 함수
        def derive_key_from_password(password, salt):
            return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        
        # 메타데이터 암호화 함수
        def encrypt_metadata(metadata_dict, password):
            salt = os.urandom(16)
            key = derive_key_from_password(password, salt)
            cipher = AES.new(key, AES.MODE_ECB)
            
            # 메타데이터를 JSON으로 변환
            metadata_json = json.dumps(metadata_dict)
            metadata_bytes = metadata_json.encode('utf-8')
            
            # 패딩
            while len(metadata_bytes) % 16 != 0:
                metadata_bytes += b'\0'
            
            encrypted = cipher.encrypt(metadata_bytes)
            return salt + encrypted
        
        # 단계 1: Caesar Cipher (시저 암호)
        def caesar_encrypt(text, shift=13):
            result = ""
            for char in text:
                if char.isalpha():
                    ascii_offset = ord('A') if char.isupper() else ord('a')
                    result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
                else:
                    result += char
            return result
        
        # 단계 2: XOR 암호화
        def xor_encrypt(text, key):
            key_bytes = key.encode('utf-8')
            result = ""
            for i, char in enumerate(text):
                result += chr(ord(char) ^ key_bytes[i % len(key_bytes)])
            return result
        
        # 단계 3: AES 암호화
        def aes_encrypt(text, key):
            # 키를 32바이트로 패딩
            key_hash = hashlib.sha256(key.encode()).digest()
            cipher = AES.new(key_hash, AES.MODE_ECB)
            
            # 텍스트를 16바이트 블록으로 패딩
            padded_text = text.encode('utf-8')
            while len(padded_text) % 16 != 0:
                padded_text += b'\0'
            
            encrypted = cipher.encrypt(padded_text)
            return encrypted
        
        # 암호화 과정
        logging.debug("암호화 진행 중...")
        
        # 1단계: Caesar Cipher
        caesar_shift = secrets.randbelow(26) + 1
        step1 = caesar_encrypt(text, caesar_shift)
        logging.debug(f"1단계 (Caesar Cipher, shift={caesar_shift}): {step1}")
        
        # 2단계: XOR 암호화
        xor_key = secrets.token_hex(8)
        step2 = xor_encrypt(step1, xor_key)
        logging.debug(f"2단계 (XOR, key={xor_key}): {step2}")
        
        # 3단계: AES 암호화
        aes_key = secrets.token_hex(16)
        step3 = aes_encrypt(step2, aes_key)
        logging.debug(f"3단계 (AES, key={aes_key}): {step3.hex()}")
        
        # 4단계: Base64 인코딩
        final_encoded = b64encode(step3).decode('utf-8')
        
        # 메타데이터 생성 및 암호화
        metadata = {
            'caesar_shift': caesar_shift,
            'xor_key': xor_key,
            'aes_key': aes_key,
            'original_length': len(text)
        }
        
        # 메타데이터를 master_password로 암호화
        encrypted_metadata = encrypt_metadata(metadata, master_password)
        encrypted_metadata_b64 = b64encode(encrypted_metadata).decode('utf-8')
        
        # 최종 결과 (암호화된 메타데이터 + 암호화된 데이터)
        result = f"SECURE_{encrypted_metadata_b64}_{final_encoded}"
        
        # n. print encoded text
        logging.debug(f"최종 암호화 완료!")
        logging.debug(f"암호화된 텍스트: {result}")
        logging.debug(f"원본 길이: {len(text)} → 암호화 길이: {len(result)}")
        logging.debug(f"메타데이터가 master_password로 암호화되었습니다.")
        
        # n. 클립보드에 복사
        try:
            pyperclip.copy(result)
            logging.debug("클립보드에 복사되었습니다! (Ctrl+V로 붙여넣기 가능)")
        except Exception as e:
            logging.debug(f"️ 클립보드 복사 실패: {str(e)}")
        
        # n. return encoded text
        return result
        
    except Exception as e:
        logging.debug(f"암호화 중 오류 발생: {str(e)}")
        return None 