def test_english_only_detection():
    """
    영어 전용 텍스트 감지 테스트
    """
    import logging
    import re
    
    def detect_language(text):
        """
        텍스트 언어 감지
        영어로만 이루어져 있으면 영어로 판단
        """
        # 영어로만 이루어져 있는지 확인 (알파벳, 공백, 구두점, 숫자만)
        english_only_pattern = re.compile(r'^[a-zA-Z\s\.,!?;:\'\"()\-0-9]+$')
        
        # 텍스트에서 영어가 아닌 문자 확인 (한글, 특수문자 등)
        non_english_chars = re.findall(r'[^a-zA-Z\s\.,!?;:\'\"()\-0-9]', text)
        
        if len(non_english_chars) == 0 and text.strip():
            return "english"
        else:
            return "korean"
    
    def get_voice_id_by_language(text):
        """
        언어에 따른 Voice ID 선택
        """
        language = detect_language(text)
        
        voice_ids = {
            "english": "EXAVITQu4vr4xnSDxMaL",  # 영어용 Voice ID
            "korean": "mYk0rAapHek2oTw18z8x",   # 한국어용 Voice ID
        }
        
        return voice_ids.get(language, "mYk0rAapHek2oTw18z8x")
    
    # 테스트 텍스트들
    test_texts = [
        "Hello, this is English text.",
        "안녕하세요. 이것은 한국어 텍스트입니다.",
        "Hello 안녕하세요",  # 혼합 텍스트
        "This is English with numbers 123",  # 영어 + 숫자
        "안녕하세요 Hello",  # 한국어 + 영어
        "1234567890",  # 숫자만
        "!@#$%^&*()",  # 특수문자만
        "",  # 빈 문자열
        "Hello world!",  # 영어 + 특수문자
        "안녕하세요 123",  # 한국어 + 숫자
    ]
    
    logging.debug("�� 영어 전용 텍스트 감지 테스트")
    
    for i, text in enumerate(test_texts, 1):
        language = detect_language(text)
        voice_id = get_voice_id_by_language(text)
        
        logging.debug(f" 테스트 {i}: {text}")
        logging.debug(f"감지된 언어: {language}")
        logging.debug(f"선택된 Voice ID: {voice_id}")
        
        # 영어가 아닌 문자 확인
        non_english_chars = re.findall(r'[^a-zA-Z\s\.,!?;:\'\"()\-0-9]', text)
        if non_english_chars:
            logging.debug(f"영어가 아닌 문자: {non_english_chars}")
        else:
            logging.debug(f"영어 전용 텍스트")
    
    logging.debug(" 영어 전용 텍스트 감지 테스트 완료!")

if __name__ == "__main__":
    test_english_only_detection() 