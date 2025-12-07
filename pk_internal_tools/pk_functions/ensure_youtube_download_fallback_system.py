from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
import logging
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pathlib import Path
import os
import json
import time
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum


class DownloadMethod(Enum):
    """다운로드 방법들을 열거형으로 정의"""
    # 1차 시도: 기본 쿠키 + 기본 옵션
    PRIMARY_COOKIE_BASIC = "primary_cookie_basic"
    
    # 2차 시도: 기본 쿠키 + 고급 옵션
    PRIMARY_COOKIE_ADVANCED = "primary_cookie_advanced"
    
    # 3차 시도: 백업 쿠키 + 기본 옵션
    BACKUP_COOKIE_BASIC = "backup_cookie_basic"
    
    # 4차 시도: 백업 쿠키 + 고급 옵션
    BACKUP_COOKIE_ADVANCED = "backup_cookie_advanced"
    
    # 5차 시도: 쿠키 없음 + 기본 옵션
    NO_COOKIE_BASIC = "no_cookie_basic"
    
    # 6차 시도: 쿠키 없음 + 고급 옵션
    NO_COOKIE_ADVANCED = "no_cookie_advanced"
    
    # 7차 시도: 브라우저에서 직접 쿠키 추출
    BROWSER_COOKIE_EXTRACT = "browser_cookie_extract"
    
    # 8차 시도: 대체 다운로더 (yt-dlp 외)
    ALTERNATIVE_DOWNLOADER = "alternative_downloader"


class CookieSource(Enum):
    """쿠키 소스를 열거형으로 정의"""
    PRIMARY_FILE = "primary_file"           # 기본 쿠키 파일
    BACKUP_FILE = "backup_file"             # 백업 쿠키 파일
    BROWSER_EXTRACT = "browser_extract"     # 브라우저에서 직접 추출
    NONE = "none"                           # 쿠키 없음


class DownloadOptions(Enum):
    """다운로드 옵션을 열거형으로 정의"""
    BASIC = "basic"                         # 기본 옵션
    ADVANCED = "advanced"                   # 고급 옵션 (User-Agent, 헤더 등)
    AGGRESSIVE = "aggressive"               # 공격적 옵션 (재시도, 타임아웃 등)


class FallbackDownloadManager:
    """
    YouTube 다운로드 실패 시 다양한 fallback 방법을 순차적으로 시도하는 관리자
    """
    
    def __init__(self):
        self.download_attempts = {}  # 각 방법별 시도 횟수 기록
        self.failure_logs = []       # 실패 로그 기록
        self.success_method = None   # 성공한 방법
        self.max_retries_per_method = 3  # 방법당 최대 재시도 횟수
        
        # 다운로드 방법 우선순위 정의
        self.download_methods_priority = [
            DownloadMethod.PRIMARY_COOKIE_BASIC,
            DownloadMethod.PRIMARY_COOKIE_ADVANCED,
            DownloadMethod.BACKUP_COOKIE_BASIC,
            DownloadMethod.BACKUP_COOKIE_ADVANCED,
            DownloadMethod.NO_COOKIE_BASIC,
            DownloadMethod.NO_COOKIE_ADVANCED,
            DownloadMethod.BROWSER_COOKIE_EXTRACT,
            DownloadMethod.ALTERNATIVE_DOWNLOADER,
        ]
        
        # 각 방법별 설정
        self.method_configs = self._initialize_method_configs()
    
    def _initialize_method_configs(self) -> Dict[DownloadMethod, Dict[str, Any]]:
        """각 다운로드 방법별 설정을 초기화"""
        configs = {}
        
        for method in DownloadMethod:
            configs[method] = {
                'cookie_source': self._get_cookie_source_for_method(method),
                'download_options': self._get_download_options_for_method(method),
                'retry_count': 0,
                'max_retries': self.max_retries_per_method,
                'enabled': True,
                'description': self._get_method_description(method)
            }
        
        return configs
    
    def _get_cookie_source_for_method(self, method: DownloadMethod) -> CookieSource:
        """메서드에 따른 쿠키 소스 결정"""
        if method in [DownloadMethod.PRIMARY_COOKIE_BASIC, DownloadMethod.PRIMARY_COOKIE_ADVANCED]:
            return CookieSource.PRIMARY_FILE
        elif method in [DownloadMethod.BACKUP_COOKIE_BASIC, DownloadMethod.BACKUP_COOKIE_ADVANCED]:
            return CookieSource.BACKUP_FILE
        elif method == DownloadMethod.BROWSER_COOKIE_EXTRACT:
            return CookieSource.BROWSER_EXTRACT
        else:
            return CookieSource.NONE
    
    def _get_download_options_for_method(self, method: DownloadMethod) -> DownloadOptions:
        """메서드에 따른 다운로드 옵션 결정"""
        if method in [DownloadMethod.PRIMARY_COOKIE_ADVANCED, DownloadMethod.BACKUP_COOKIE_ADVANCED, 
                     DownloadMethod.NO_COOKIE_ADVANCED]:
            return DownloadOptions.ADVANCED
        elif method == DownloadMethod.ALTERNATIVE_DOWNLOADER:
            return DownloadOptions.AGGRESSIVE
        else:
            return DownloadOptions.BASIC
    
    def _get_method_description(self, method: DownloadMethod) -> str:
        """메서드별 설명 반환"""
        descriptions = {
            DownloadMethod.PRIMARY_COOKIE_BASIC: "기본 쿠키 + 기본 옵션",
            DownloadMethod.PRIMARY_COOKIE_ADVANCED: "기본 쿠키 + 고급 옵션",
            DownloadMethod.BACKUP_COOKIE_BASIC: "백업 쿠키 + 기본 옵션",
            DownloadMethod.BACKUP_COOKIE_ADVANCED: "백업 쿠키 + 고급 옵션",
            DownloadMethod.NO_COOKIE_BASIC: "쿠키 없음 + 기본 옵션",
            DownloadMethod.NO_COOKIE_ADVANCED: "쿠키 없음 + 고급 옵션",
            DownloadMethod.BROWSER_COOKIE_EXTRACT: "브라우저에서 직접 쿠키 추출",
            DownloadMethod.ALTERNATIVE_DOWNLOADER: "대체 다운로더 사용",
        }
        return descriptions.get(method, "알 수 없는 방법")
    
    def download_with_fallback(self, url: str, output_dir: str) -> Tuple[bool, Optional[str]]:
        """
        fallback 시스템을 사용하여 다운로드 시도
        
        Args:
            url: 다운로드할 YouTube URL
            output_dir: 출력 디렉토리
            
        Returns:
            Tuple[bool, Optional[str]]: (성공 여부, 성공한 방법 또는 실패 이유)
        """
        logging.debug("YouTube 다운로드 Fallback 시스템 시작")
        logging.debug(f"다운로드 URL: {url}")
        logging.debug(f"출력 디렉토리: {output_dir}")
        
        # 각 방법을 우선순위에 따라 순차적으로 시도
        for method in self.download_methods_priority:
            if not self.method_configs[method]['enabled']:
                logging.debug(f"️ {method.value} 비활성화됨, 건너뜀")
                continue
            
            logging.debug(f"{self.method_configs[method]['description']} 시도 중...")
            
            # 해당 방법으로 다운로드 시도
            success, result = self._attempt_download_with_method(method, url, output_dir)
            
            if success:
                self.success_method = method.value
                logging.debug(f"다운로드 성공: {self.method_configs[method]['description']}")
                return True, method.value
            else:
                # 실패 로그 기록
                self._log_failure(method, url, result)
                logging.debug(f"{self.method_configs[method]['description']} 실패: {result}")
                
                # 최대 재시도 횟수 확인
                if self.method_configs[method]['retry_count'] >= self.max_retries_per_method:
                    logging.debug(f"️ {method.value} 최대 재시도 횟수 도달, 다음 방법으로 진행")
                    self.method_configs[method]['enabled'] = False
        
        # 모든 방법 실패
        failure_summary = self._generate_failure_summary()
        logging.debug("모든 다운로드 방법 실패")
        logging.debug(failure_summary)
        
        return False, failure_summary
    
    def _attempt_download_with_method(self, method: DownloadMethod, url: str, output_dir: str) -> Tuple[bool, str]:
        """특정 방법으로 다운로드 시도"""
        try:
            # 재시도 횟수 증가
            self.method_configs[method]['retry_count'] += 1
            
            # 쿠키 소스 결정
            cookie_source = self.method_configs[method]['cookie_source']
            cookie_file = self._get_cookie_file(cookie_source)
            
            # 다운로드 옵션 결정
            download_options = self.method_configs[method]['download_options']
            ydl_opts = self._create_ydl_opts(download_options, cookie_file, output_dir)
            
            # 실제 다운로드 실행
            if method == DownloadMethod.ALTERNATIVE_DOWNLOADER:
                success, result = self._download_with_alternative_downloader(url, output_dir)
            else:
                success, result = self._download_with_yt_dlp(url, ydl_opts)
            
            return success, result
            
        except Exception as e:
            return False, f"메서드 실행 중 오류: {str(e)}"
    
    def _get_cookie_file(self, cookie_source: CookieSource) -> Optional[str]:
        """쿠키 소스에 따른 쿠키 파일 경로 반환"""
        from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
        
        if cookie_source == CookieSource.NONE:
            return None
        
        cookie_dir = d_pk_root_hidden
        
        if cookie_source == CookieSource.PRIMARY_FILE:
            cookie_file = cookie_dir / "chrome_youtube_cookies.txt"
            if cookie_file.exists() and cookie_file.stat().st_size > 0:
                return str(cookie_file)
            return None
        
        elif cookie_source == CookieSource.BACKUP_FILE:
            # 백업 쿠키 파일 찾기
            backup_files = list(cookie_dir.glob("chrome_youtube_cookies_backup_*.txt"))
            if backup_files:
                latest_backup = max(backup_files, key=lambda f: f.stat().st_mtime)
                return str(latest_backup)
            return None
        
        elif cookie_source == CookieSource.BROWSER_EXTRACT:
            # 브라우저에서 쿠키 추출 시도
            return self._extract_cookies_from_browser()
        
        return None
    
    def _extract_cookies_from_browser(self) -> Optional[str]:
        """브라우저에서 쿠키 추출"""
        try:
            from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
            
            cookie_dir = d_pk_root_hidden
            temp_cookie_file = cookie_dir / "temp_browser_cookies.txt"
            
            # yt-dlp를 사용하여 Chrome에서 쿠키 추출
            cmd = [
                "yt-dlp",
                "--cookies-from-browser", "chrome",
                "--cookies", str(temp_cookie_file),
                "--print", "id",
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and temp_cookie_file.exists() and temp_cookie_file.stat().st_size > 0:
                return str(temp_cookie_file)
            
            return None
            
        except Exception as e:
            logging.debug(f"브라우저 쿠키 추출 실패: {e}")
            return None
    
    def _create_ydl_opts(self, download_options: DownloadOptions, cookie_file: Optional[str], output_dir: str) -> Dict[str, Any]:
        """다운로드 옵션에 따른 yt-dlp 옵션 생성"""
        base_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s [%(id)s].%(ext)s'),
            'quiet': False,
            'noplaylist': True,
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'geo_bypass': True,
        }
        
        # 쿠키 파일이 있으면 추가
        if cookie_file:
            base_opts['cookiefile'] = cookie_file
        
        if download_options == DownloadOptions.BASIC:
            return base_opts
        
        elif download_options == DownloadOptions.ADVANCED:
            base_opts.update({
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'add_headers': {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Accept-Encoding': 'gzip,deflate',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                },
                'retries': 3,
                'fragment_retries': 3,
                'extractor_retries': 3,
            })
        
        elif download_options == DownloadOptions.AGGRESSIVE:
            base_opts.update({
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'add_headers': {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Accept-Encoding': 'gzip,deflate',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                },
                'retries': 10,
                'fragment_retries': 10,
                'extractor_retries': 10,
                'retry_sleep': 1,
                'max_sleep_interval': 5,
                'socket_timeout': 30,
                'extractor_timeout': 60,
                'no_check_certificate': True,
                'prefer_insecure': True,
            })
        
        return base_opts
    
    def _download_with_yt_dlp(self, url: str, ydl_opts: Dict[str, Any]) -> Tuple[bool, str]:
        """yt-dlp를 사용한 다운로드"""
        try:
            import yt_dlp
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 정보 추출
                info = ydl.extract_info(url, download=False)
                if not info:
                    return False, "동영상 정보 추출 실패"
                
                # 다운로드 실행
                ydl.download([url])
                
                # 다운로드 확인 (간단한 검증)
                video_id = info.get('id')
                if video_id:
                    # 다운로드된 파일 확인
                    output_template = ydl_opts.get('outtmpl', '%(title)s [%(id)s].%(ext)s')
                    expected_filename = output_template.replace('%(title)s', info.get('title', 'Unknown')).replace('%(id)s', video_id)
                    
                    if os.path.exists(expected_filename):
                        return True, "yt-dlp 다운로드 성공"
                    else:
                        return False, "다운로드된 파일을 찾을 수 없음"
                
                return True, "yt-dlp 다운로드 성공"
                
        except Exception as e:
            return False, f"yt-dlp 다운로드 오류: {str(e)}"
    
    def _download_with_alternative_downloader(self, url: str, output_dir: str) -> Tuple[bool, str]:
        """대체 다운로더를 사용한 다운로드"""
        try:
            # 여러 대체 다운로더 시도
            alternative_downloaders = [
                ("yt-dlp (최신)", ["yt-dlp", "--update"]),
                ("youtube-dl", ["youtube-dl"]),
                ("yt-dlp (강제 옵션)", ["yt-dlp", "--force-ipv4", "--no-check-certificate"]),
            ]
            
            for name, cmd in alternative_downloaders:
                try:
                    # 다운로드 명령 구성
                    download_cmd = cmd + [
                        "-f", "best",
                        "-o", os.path.join(output_dir, "%(title)s [%(id)s].%(ext)s"),
                        url
                    ]
                    
                    logging.debug(f"{name} 시도 중...")
                    
                    result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=120)
                    
                    if result.returncode == 0:
                        return True, f"{name} 다운로드 성공"
                    
                except Exception as e:
                    continue
            
            return False, "모든 대체 다운로더 실패"
            
        except Exception as e:
            return False, f"대체 다운로더 실행 오류: {str(e)}"
    
    def _log_failure(self, method: DownloadMethod, url: str, error_msg: str):
        """실패 로그 기록"""
        failure_log = {
            'timestamp': datetime.now().isoformat(),
            'method': method.value,
            'method_description': self.method_configs[method]['description'],
            'url': url,
            'error_message': error_msg,
            'retry_count': self.method_configs[method]['retry_count'],
            'cookie_source': self.method_configs[method]['cookie_source'].value,
            'download_options': self.method_configs[method]['download_options'].value,
        }
        
        self.failure_logs.append(failure_log)
    
    def _generate_failure_summary(self) -> str:
        """실패 요약 생성"""
        if not self.failure_logs:
            return "실패 로그가 없습니다."
        
        summary_lines = [" 다운로드 실패 요약:"]
        
        # 방법별 실패 통계
        method_failures = {}
        for log in self.failure_logs:
            method = log['method']
            if method not in method_failures:
                method_failures[method] = 0
            method_failures[method] += 1
        
        for method, count in method_failures.items():
            summary_lines.append(f"  • {method}: {count}회 실패")
        
        # 상세 실패 로그
        summary_lines.append("\n 상세 실패 로그:")
        for i, log in enumerate(self.failure_logs[-5:], 1):  # 최근 5개만
            summary_lines.append(f"  {i}. {log['method_description']}: {log['error_message']}")
        
        return "\n".join(summary_lines)
    
    def get_statistics(self) -> Dict[str, Any]:
        """다운로드 통계 반환"""
        total_attempts = sum(config['retry_count'] for config in self.method_configs.values())
        successful_methods = [method.value for method in DownloadMethod if self.method_configs[method]['retry_count'] > 0]
        
        return {
            'total_attempts': total_attempts,
            'successful_method': self.success_method,
            'failure_logs_count': len(self.failure_logs),
            'method_attempts': {method.value: config['retry_count'] for method, config in self.method_configs.items()},
            'enabled_methods': [method.value for method in DownloadMethod if self.method_configs[method]['enabled']],
        }
    
    def reset_statistics(self):
        """통계 초기화"""
        self.download_attempts = {}
        self.failure_logs = []
        self.success_method = None
        
        for config in self.method_configs.values():
            config['retry_count'] = 0
            config['enabled'] = True


@ensure_seconds_measured
def ensure_youtube_download_with_fallback(url: str, output_dir: str = None) -> bool:
    """
    YouTube 동영상을 fallback 시스템을 사용하여 다운로드
    
    Args:
        url: 다운로드할 YouTube URL
        output_dir: 출력 디렉토리 (None이면 기본 디렉토리 사용)
        
    Returns:
        bool: 다운로드 성공 여부
    """
    if output_dir is None:
        from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
        output_dir = D_PK_WORKING
    
    # 출력 디렉토리 생성
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Fallback 다운로드 매니저 생성
    fallback_manager = FallbackDownloadManager()
    
    # 다운로드 시도
    success, result = fallback_manager.download_with_fallback(url, output_dir)
    
    if success:
        logging.debug(f"다운로드 성공! 사용된 방법: {result}")
        
        # 통계 출력
        stats = fallback_manager.get_statistics()
        logging.debug(f"총 시도 횟수: {stats['total_attempts']}")
        
    else:
        logging.debug(f"다운로드 실패: {result}")
        
        # 실패 통계 출력
        stats = fallback_manager.get_statistics()
        logging.debug(f"총 시도 횟수: {stats['total_attempts']}")
        logging.debug(f"실패 로그 수: {stats['failure_logs_count']}")
    
    return success

