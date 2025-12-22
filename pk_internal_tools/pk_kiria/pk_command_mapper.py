"""
명령어 매핑 관련 클래스들
DynamicCommandMapper와 ProcessMatcher를 제공합니다.
"""
import datetime
import logging
import os
import re
from typing import List, Tuple

from pk_internal_tools.pk_functions.get_sorted_pk_files import get_excutable_pk_wrappers

logger = logging.getLogger(__name__)


class DynamicCommandMapper:
    """동적 명령어-함수 매핑 클래스"""

    def __init__(self):
        self.mapping = {}
        self.cache_timestamp = None
        self.cache_duration = 300  # 5분 캐시
        self._refresh_mappings()

    def _refresh_mappings(self):
        """pk_external_tools 하위의 모든 파일에서 함수명을 추출해 동적 매핑 생성"""
        self.mapping = {}
        base_dir = os.path.join(os.path.dirname(__file__), '..')
        pk_external_tools_dir = os.path.abspath(os.path.join(base_dir, '..', 'pk_external_tools'))

        for root, dirs, files in os.walk(pk_external_tools_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, encoding='utf-8') as f:
                            content = f.read()
                        # 함수명 추출 (def 함수명)
                        for match in re.finditer(r'def\s+([a-zA-Z0-9_]+)\s*\(', content):
                            func_name = match.group(1)
                            # 형태소 분석 대신 언더스코어/영어 단어 분리
                            tokens = re.split(r'[_]', func_name)
                            for token in tokens:
                                if len(token) > 1:  # 한 글자 토큰은 제외
                                    self.mapping.setdefault(token.lower(), set()).add(func_name)
                            # 전체 함수명도 매핑
                            self.mapping.setdefault(func_name.lower(), set()).add(func_name)
                    except Exception as e:
                        pass  # 파일 읽기 실패는 무시

        # set → list 변환
        for k in self.mapping:
            self.mapping[k] = list(self.mapping[k])

    def find_matching_functions(self, command: str):
        """명령어에 매칭되는 함수명(들) 반환"""
        self._refresh_mappings()
        command_lower = command.lower().strip()
        matches = set()
        # 완전 일치
        if command_lower in self.mapping:
            matches.update(self.mapping[command_lower])
        # 부분 일치 (토큰)
        for key in self.mapping:
            if key in command_lower or command_lower in key:
                matches.update(self.mapping[key])
        return list(matches)

    def print_current_mapping(self, command: str):
        matches = self.find_matching_functions(command)
        logging.debug(f"[동적 함수 매핑] '{command}' → {matches if matches else '매칭 없음'}")


class ProcessMatcher:
    """PK 프로세스와 자연어 명령어 매칭 클래스"""

    def __init__(self):
        self.process_cache = {}
        self.cache_timestamp = None
        self.cache_duration = 300  # 5분 캐시
        self.dynamic_mapper = DynamicCommandMapper()

    def get_process_names(self) -> List[str]:
        """PK 프로세스 목록 가져오기 (캐시 적용)"""
        now = datetime.datetime.now()
        if (self.cache_timestamp is None or
                (now - self.cache_timestamp).seconds > self.cache_duration):
            try:
                pk_wrappers = get_excutable_pk_wrappers()
                import os
                # pk_ prefix 제거하고 파일명만 추출
                process_names = []
                for file_path in pk_wrappers:
                    file_name = os.path.basename(file_path).replace('.py', '')
                    # pk_ prefix 제거
                    if file_name.startswith('pk_'):
                        clean_name = file_name[3:]  # pk_ 제거
                    else:
                        clean_name = file_name
                    process_names.append(clean_name)

                self.process_cache = process_names
                self.cache_timestamp = now
            except Exception as e:
                logging.debug(f"️ 프로세스 목록 가져오기 오류: {e}")
                return []

        return self.process_cache

    def analyze_morphemes(self, text: str) -> List[str]:
        """형태소 분석 (konlpy 사용)"""
        try:
            from konlpy.tag import Okt
            okt = Okt()

            # 명사, 동사, 형용사 추출
            nouns = okt.nouns(text)
            verbs = okt.verbs(text)
            adjectives = okt.adjectives(text)

            # 모든 형태소 합치기
            morphemes = nouns + verbs + adjectives

            # 중복 제거 및 빈 문자열 제거
            morphemes = list(set([m for m in morphemes if m.strip()]))

            return morphemes

        except ImportError:
            # konlpy가 없는 경우 개선된 단순 분리
            logging.debug("️ konlpy가 설치되지 않아 개선된 단순 분리로 대체합니다.")
            return self._improved_simple_tokenize(text)
        except Exception as e:
            logging.debug(f"️ 형태소 분석 오류: {e}")
            return self._improved_simple_tokenize(text)

    def _improved_simple_tokenize(self, text: str) -> List[str]:
        """개선된 단순 토큰화 (konlpy 없을 때 사용)"""
        import re

        # n. 한글, 영문, 숫자만 추출 (특수문자 제거)
        tokens = re.findall(r'[가-힣a-zA-Z0-9]+', text)

        # n. 2글자 이상만 유지
        tokens = [token for token in tokens if len(token) > 1]

        # n. 한국어 조사 제거
        korean_particles = ['은', '는', '이', '가', '을', '를', '의', '에', '에서', '로', '으로', '와', '과', '도', '만', '부터', '까지', '처럼', '같이', '보다', '마다', '당', '씩', '마다', '당', '씩']
        tokens = [token for token in tokens if token not in korean_particles]

        # n. 일반적인 불용어 제거
        stop_words = ['그', '이', '저', '것', '수', '등', '때', '곳', '말', '일', '년', '월', '일', '시', '분', '초']
        tokens = [token for token in tokens if token not in stop_words]

        return tokens

    def calculate_similarity_between_user_comand_and_process_name(self, user_command: str, process_name: str) -> float:
        """사용자 명령어와 프로세스명 간의 유사도 계산"""
        try:
            # 사용자 명령어 형태소 분석
            user_morphemes = self.analyze_morphemes(user_command.lower())

            # 프로세스명 형태소 분석
            process_morphemes = self.analyze_morphemes(process_name.lower())

            if not user_morphemes or not process_morphemes:
                return 0.0

            # 공통 형태소 수 계산
            common_morphemes = set(user_morphemes) & set(process_morphemes)

            # Jaccard 유사도 계산
            union_morphemes = set(user_morphemes) | set(process_morphemes)

            if not union_morphemes:
                return 0.0

            similarity = len(common_morphemes) / len(union_morphemes)

            # 추가 가중치: 정확한 부분 문자열 매칭
            if any(morpheme in process_name.lower() for morpheme in user_morphemes):
                similarity += 0.2

            # 추가 가중치: 키워드 매칭
            keywords = {
                '크롬': ['chrome', 'browser', '웹'],
                '열기': ['open', 'start', '실행'],
                '파일': ['file', 'document'],
                '백업': ['backup', 'save', '저장'],
                '정리': ['clean', 'clear', '정리'],
                '시스템': ['system', 'os'],
                '프로세스': ['process', 'task'],
                '종료': ['kill', 'stop', 'end'],
                '확인': ['check', 'verify', 'status'],
                '설정': ['config', 'setting', 'option']
            }

            for user_word in user_morphemes:
                for keyword, related_words in keywords.items():
                    if user_word in keyword or keyword in user_word:
                        for related_word in related_words:
                            if related_word in process_name.lower():
                                similarity += 0.3
                                break

            return min(similarity, 1.0)

        except Exception as e:
            logging.debug(f"️ 유사도 계산 오류: {e}")
            return 0.0

    def find_similar_processes(self, user_command: str, threshold: float = 0.1) -> List[Tuple[str, float]]:
        """사용자 명령어와 유사한 프로세스들 찾기"""
        process_names = self.get_process_names()
        similar_processes = []

        for process_name in process_names:
            similarity = self.calculate_similarity_between_user_comand_and_process_name(user_command, process_name)
            if similarity >= threshold:
                similar_processes.append((process_name, similarity))

        # 유사도 순으로 정렬
        similar_processes.sort(key=lambda x: x[1], reverse=True)

        return similar_processes

    def find_dynamic_matches(self, command: str):
        """동적 매핑을 통한 함수 찾기"""
        return self.dynamic_mapper.find_matching_functions(command)

    def print_dynamic_mapping(self, command: str):
        """동적 매핑 정보 출력"""
        self.dynamic_mapper.print_current_mapping(command)

