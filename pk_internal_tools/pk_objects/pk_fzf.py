
from typing import List, Optional

class PkFzf:
    """초고속 fzf 처리기"""

    def __init__(self, fzf_cmd, files, last_choice=None, custom_fzf_options: Optional[List[str]] = None):
        from pk_internal_tools.pk_functions.get_nx import get_nx

        from pk_internal_tools.pk_objects.pk_texts import PK_WRAPPER_PREFIX
        self.fzf_executable_command = fzf_cmd
        self.files = files
        self.last_selected = last_choice
        self.file_names_to_display = [get_nx(p).removeprefix(PK_WRAPPER_PREFIX) for p in files]
        self.custom_fzf_options = custom_fzf_options or []

    def build_ultra_fast_fzf_command(self):
        from pk_internal_tools.pk_functions.get_nx import get_nx

        from pk_internal_tools.pk_functions.get_pk_fzf_options import get_pk_fzf_options
        from pk_internal_tools.pk_objects.pk_texts import PK_WRAPPER_PREFIX
        """초고속 fzf 명령어 구성"""

        cmd = [self.fzf_executable_command] + get_pk_fzf_options()

        # 마지막 선택 파일 쿼리 설정
        if self.last_selected and self.last_selected in self.file_names_to_display:
            cmd += ["--query", self.last_selected]
        
        if self.custom_fzf_options: # Append custom options
            cmd.extend(self.custom_fzf_options)

        return cmd

    def run_ultra_fast_fzf(self):
        import subprocess
        import sys
        import os
        import logging
        from pk_internal_tools.pk_functions.get_os_n import get_os_n
        from pk_internal_tools.pk_functions.ensure_chcp_65001 import ensure_chcp_65001
        
        """초고속 fzf 실행"""
        fzf_input = '\n'.join(self.file_names_to_display)
        cmd = self.build_ultra_fast_fzf_command()

        # Windows에서 한글 인코딩 문제 해결
        if get_os_n() == 'windows':
            ensure_chcp_65001()
            # stdout/stderr 인코딩 설정
            try:
                sys.stdout.reconfigure(encoding='utf-8')
                sys.stderr.reconfigure(encoding='utf-8')
            except Exception as e:
                pass  # 이미 설정되어 있거나 설정할 수 없는 경우 무시
        
        # 환경변수 설정 (Windows에서 UTF-8 지원)
        env = os.environ.copy()
        if get_os_n() == 'windows':
            env['PYTHONIOENCODING'] = 'utf-8'
            env['LANG'] = 'ko_KR.UTF-8'
            env['LC_ALL'] = 'ko_KR.UTF-8'

        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',  # 명시적으로 UTF-8 인코딩 설정
            errors='replace',  # 인코딩 오류 시 대체 문자 사용
            env=env,  # 환경변수 전달
            #  추가 최적화
            bufsize=1,  # 라인 버퍼링
            universal_newlines=True,  # 텍스트 모드
        )

        logging.debug(f"UI 렌더링 시작")
        logging.debug(f"파일을 선택하고 Enter를 눌러주세요")

        # 사용자 입력 대기 (UTF-8로 인코딩된 문자열 전달)
        try:
            out, err = proc.communicate(input=fzf_input)
        except UnicodeEncodeError:
            # 인코딩 오류 발생 시 UTF-8로 명시적으로 인코딩
            fzf_input_bytes = fzf_input.encode('utf-8')
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )
            out_bytes, err_bytes = proc.communicate(input=fzf_input_bytes)
            out = out_bytes.decode('utf-8', errors='replace')
            err = err_bytes.decode('utf-8', errors='replace')

        return proc.returncode, out.strip(), err
