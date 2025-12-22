from typing import List

def extract_korean_nouns(text: str) -> List[str]:
    """
    입력된 한국어 텍스트에서 명사를 추출하여 리스트로 반환합니다.
    KoNLPy의 Okt 형태소 분석기를 사용하며, Java 환경을 자동으로 설정합니다.

    Args:
        text (str): 명사를 추출할 한국어 텍스트.

    Returns:
        List[str]: 추출된 명사 리스트.
    """
    from .ensure_java_home_configured import ensure_java_home_configured
    from .ensure_java_installed import ensure_java_installed # New import
    import logging

    # n. Java가 설치되어 있고 PATH에 등록되어 있는지 확인
    if not ensure_java_installed():
        logging.error("Java가 설치되지 않았거나 PATH에 등록되지 않았습니다. 명사 추출 불가.")
        return []

    # n. JAVA_HOME 환경 변수 설정 확인 및 자동 설정
    if not ensure_java_home_configured():
        logging.error("JAVA_HOME 환경 변수 설정에 실패했습니다. 명사 추출 불가.")
        return []

    try:
        from konlpy.tag import Okt
        okt = Okt()
        nouns = okt.nouns(text)
        # 한 글자 명사 제외 및 중복 제거
        unique_nouns = list(set(noun for noun in nouns if len(noun) > 1))
        return unique_nouns
    except ImportError:
        logging.error("KoNLPy 라이브러리가 설치되지 않았습니다. 명사 추출 불가.")
        return []
    except Exception as e:
        logging.error(f"명사 추출 중 오류 발생: {e}", exc_info=True)
        return []

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    test_text = "안녕하세요. 저는 한국어 명사 추출 테스트를 진행하고 있습니다. 파이썬과 KoNLPy를 사용합니다."
    print(f"테스트 텍스트: {test_text}")
    extracted_nouns = extract_korean_nouns(test_text)
    print(f"추출된 명사: {extracted_nouns}")

    test_text_2 = "사과, 바나나, 컴퓨터, 프로그래밍, 안녕하세요."
    print(f"\n테스트 텍스트 2: {test_text_2}")
    extracted_nouns_2 = extract_korean_nouns(test_text_2)
    print(f"추출된 명사 2: {extracted_nouns_2}")
