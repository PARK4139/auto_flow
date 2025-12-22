"""
Xavier에서 kiri 서버를 시작하는 함수
음성인식 기반 제어를 위한 kiri 서버 실행 및 마이크 설치 가이드 포함
"""

import logging
import tempfile
import textwrap
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_text_yellow import get_text_yellow
from pk_internal_tools.pk_objects.pk_remote_target_controller import (
    PkRemoteTargetEngine,
    PkModes2,
)

logger = logging.getLogger(__name__)


def _get_microphone_setup_guide() -> str:
    """마이크 설치 가이드 텍스트 반환"""
    return textwrap.dedent("""
    ========================================
    Xavier 마이크 설치 가이드
    ========================================
    
    ## 1. 물리적 마이크 연결 확인
    
    ### USB 마이크를 사용하는 경우:
    1. USB 마이크를 Xavier의 USB 포트에 연결
    2. 연결 확인:
       ```bash
       lsusb | grep -i "audio\|microphone\|mic"
       ```
    3. 오디오 장치 확인:
       ```bash
       arecord -l
       ```
    
    ### 내장 마이크를 사용하는 경우:
    1. Xavier에 내장 마이크가 있는지 확인
    2. 오디오 장치 확인:
       ```bash
       arecord -l
       ```
    
    ## 2. 오디오 시스템 확인
    
    ### ALSA 확인:
    ```bash
    # 오디오 장치 목록
    arecord -l
    
    # 오디오 장치 테스트
    arecord -d 3 -f cd test.wav
    aplay test.wav
    ```
    
    ### PulseAudio 확인 (설치된 경우):
    ```bash
    # PulseAudio 서비스 상태
    systemctl --user status pulseaudio
    
    # 오디오 장치 목록
    pactl list sources short
    ```
    
    ## 3. Python 음성 인식 라이브러리 설치
    
    ```bash
    # 필수 패키지 설치
    sudo apt-get update
    sudo apt-get install -y python3-pip portaudio19-dev python3-pyaudio
    
    # Python 라이브러리 설치
    pip3 install SpeechRecognition pyaudio
    ```
    
    ## 4. 마이크 테스트
    
    ```bash
    # Python으로 마이크 테스트
    python3 -c "
    import speech_recognition as sr
    r = sr.Recognizer()
    mics = sr.Microphone.list_microphone_names()
    print('감지된 마이크:', mics)
    "
    ```
    
    ## 5. 문제 해결
    
    ### 마이크가 감지되지 않는 경우:
    1. USB 마이크를 다른 포트에 연결 시도
    2. USB 마이크가 호환되는지 확인 (USB Audio Class 지원)
    3. 드라이버 설치:
       ```bash
       sudo apt-get install -y alsa-utils
       ```
    
    ### 권한 문제:
    ```bash
    # 사용자를 audio 그룹에 추가
    sudo usermod -a -G audio $USER
    # 재로그인 필요
    ```
    
    ========================================
    """)


def _check_microphone_on_remote_target(controller: PkRemoteTargetEngine) -> bool:
    """Xavier에서 마이크가 사용 가능한지 확인"""
    logger.info("Xavier에서 마이크 확인 중...")
    
    # 1. USB 마이크 확인
    logger.info("1. USB 마이크 확인 중...")
    stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
        cmd="lsusb | grep -i 'audio\\|microphone\\|mic' || echo 'USB 마이크 미감지'",
        timeout_seconds=10,
        use_sudo=False,
    )
    if stdout:
        for line in stdout:
            logger.info("  %s", line)
    
    # 2. ALSA 오디오 장치 확인
    logger.info("2. ALSA 오디오 장치 확인 중...")
    stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
        cmd="arecord -l 2>/dev/null || echo 'arecord 명령어 없음 (alsa-utils 설치 필요)'",
        timeout_seconds=10,
        use_sudo=False,
    )
    if stdout:
        for line in stdout:
            logger.info("  %s", line)
    
    # 3. Python으로 마이크 확인
    logger.info("3. Python으로 마이크 확인 중...")
    mic_check_script = """
import sys
try:
    import speech_recognition as sr
    r = sr.Recognizer()
    mics = sr.Microphone.list_microphone_names()
    if mics:
        print(f"감지된 마이크: {len(mics)}개")
        for i, mic in enumerate(mics):
            print(f"  [{i}] {mic}")
        sys.exit(0)
    else:
        print("마이크가 감지되지 않았습니다.")
        sys.exit(1)
except ImportError:
    print("SpeechRecognition 라이브러리가 설치되지 않았습니다.")
    sys.exit(2)
except Exception as e:
    print(f"마이크 확인 중 오류: {e}")
    sys.exit(3)
"""
    
    # 임시 스크립트 생성 및 전송
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py', encoding='utf-8') as f:
        temp_script = f.name
        f.write(mic_check_script)
    
    try:
        remote_script = "/tmp/check_mic.py"
        ok = controller.ensure_file_transferred_to_remote_target(temp_script, remote_script)
        if ok:
            stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
                cmd=f"python3 {remote_script}",
                timeout_seconds=15,
                use_sudo=False,
            )
            if stdout:
                for line in stdout:
                    logger.info("  %s", line)
            
            if exit_code == 0:
                logger.info("✅ 마이크가 감지되었습니다.")
                return True
            elif exit_code == 2:
                logger.warning("⚠️ SpeechRecognition 라이브러리가 설치되지 않았습니다.")
                return False
            else:
                logger.warning("⚠️ 마이크가 감지되지 않았습니다.")
                return False
        else:
            logger.warning("⚠️ 마이크 확인 스크립트 전송 실패")
            return False
    finally:
        import os
        if os.path.exists(temp_script):
            try:
                os.remove(temp_script)
            except Exception as e:
                pass
    
    return False


def _ensure_microphone_dependencies_on_remote_target(controller: PkRemoteTargetEngine) -> bool:
    """Xavier에 마이크 사용을 위한 필수 패키지 설치"""
    logger.info("마이크 사용을 위한 필수 패키지 설치 중...")
    
    # 1. 시스템 패키지 설치
    packages = [
        "alsa-utils",
        "portaudio19-dev",
        "python3-pyaudio",
    ]
    
    for package in packages:
        logger.info("  - %s 설치 중...", package)
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=f"sudo apt-get install -y {package}",
            timeout_seconds=120,
            use_sudo=True,
        )
        if exit_code != 0:
            logger.warning("  ⚠️ %s 설치 실패 (계속 진행)", package)
    
    # 2. Python 라이브러리 설치
    logger.info("  - Python 음성 인식 라이브러리 설치 중...")
    stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
        cmd="pip3 install SpeechRecognition pyaudio",
        timeout_seconds=120,
        use_sudo=False,
    )
    if exit_code != 0:
        logger.warning("  ⚠️ Python 라이브러리 설치 실패")
        if stderr:
            for line in stderr:
                logger.debug("    %s", line)
    
    # 3. 오디오 그룹에 사용자 추가
    logger.info("  - 오디오 그룹 권한 확인 중...")
    stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
        cmd="groups | grep -q audio || echo 'audio 그룹에 추가 필요'",
        timeout_seconds=10,
        use_sudo=False,
    )
    if stdout and any("추가 필요" in line for line in stdout):
        logger.info("  - 사용자를 audio 그룹에 추가 중...")
        user = getattr(controller.remote_target, "user_n", "pk")
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=f"sudo usermod -a -G audio {user}",
            timeout_seconds=10,
            use_sudo=True,
        )
        if exit_code == 0:
            logger.info("  ✅ audio 그룹에 추가되었습니다. (재로그인 필요할 수 있음)")
    
    return True


def _get_kiria_server_script_content() -> str:
    """Xavier에서 실행할 kiri 서버 스크립트 내용 반환"""
    return textwrap.dedent("""
#!/usr/bin/env python3

\"\"\"
Xavier에서 실행되는 kiri 서버 스크립트
음성인식 기반 제어 서버
\"\"\"
import sys
import os
from pathlib import Path

# 프로젝트 경로 추가
pk_root = Path.home() / "pk_system"
if (pk_root / "pk_internal_tools").exists():
    sys.path.insert(0, str(pk_root))
    sys.path.insert(0, str(pk_root / "pk_internal_tools"))

# 로깅 초기화
try:
    from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
    ensure_pk_system_log_initialized(__file__)
except Exception as e:
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] [%(message)s]'
    )

logger = logging.getLogger(__name__)

# kiri 실행
try:
    from pk_internal_tools.pk_kiria.ensure_pk_kiria_executed_on_remote_target import ensure_pk_kiria_executed_on_remote_target
    logger.info("kiri 서버 시작 중...")
    ensure_pk_kiria_executed_on_remote_target()
except ImportError as e:
    logger.error("kiri 모듈을 찾을 수 없습니다: %s", e)
    logger.info("프로젝트 경로 확인: %s", pk_root)
    sys.exit(1)
except Exception as e:
    logger.error("kiri 서버 실행 중 오류: %s", e, exc_info=True)
    sys.exit(1)
""")


def ensure_kiria_server_started_on_remote_target(
    remote_target_ip: Optional[str] = None,
    remote_target_user: Optional[str] = None,
    remote_target_pw: Optional[str] = None,
    skip_mic_check: bool = False,
) -> bool:
    """
    Xavier에서 kiri 서버를 시작합니다.
    
    Args:
        remote_target_ip: remote_target_ip 주소. None이면 환경변수 또는 입력받기
        remote_target_user: Xavier 사용자명. None이면 환경변수 또는 입력받기
        remote_target_pw: Xavier 비밀번호. None이면 환경변수 또는 입력받기
        skip_mic_check: 마이크 확인을 건너뛸지 여부
        
    Returns:
        bool: 서버 시작 성공 여부
    """
    try:
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
        
        # remote_target 연결 정보 가져오기
        if not remote_target_ip:
            remote_target_ip = ensure_env_var_completed("XAVIER_IP")
        if not remote_target_user:
            remote_target_user = ensure_env_var_completed("XAVIER_USER")
        if not remote_target_pw:
            remote_target_pw = ensure_env_var_completed("XAVIER_PW")
        
        # Xavier 컨트롤러 생성
        controller = PkRemoteTargetEngine(
            
            ip=remote_target_ip,
            user_n=remote_target_user,
            pw=remote_target_pw,
        )
        
        logger.info("=" * 60)
        logger.info("kiri 서버 시작 (Xavier)")
        logger.info("=" * 60)
        
        # 1. 마이크 설치 가이드 표시
        logger.info("\\n" + _get_microphone_setup_guide())
        
        # 2. 마이크 확인 (건너뛰지 않는 경우)
        mic_available = False
        if not skip_mic_check:
            mic_available = _check_microphone_on_remote_target(controller)
            
            if not mic_available:
                logger.warning("⚠️ 마이크가 감지되지 않았습니다.")
                logger.info("마이크 설치 가이드를 참고하여 마이크를 연결하고 다시 시도하세요.")
                
                # 필수 패키지 설치 시도
                logger.info("필수 패키지 설치를 시도합니다...")
                _ensure_microphone_dependencies_on_remote_target(controller)
                
                # 다시 확인
                logger.info("마이크를 다시 확인합니다...")
                mic_available = _check_microphone_on_remote_target(controller)
                
                if not mic_available:
                    logger.warning("⚠️ 마이크가 여전히 감지되지 않습니다.")
                    logger.info(get_text_yellow("마이크 없이도 서버는 시작할 수 있지만, 음성 인식 기능은 사용할 수 없습니다."))
                    response = input("continue:y/n").strip().lower()
                    if response != 'y':
                        logger.info("사용자가 취소했습니다.")
                        return False
        else:
            logger.info("마이크 확인을 건너뜁니다.")
        
        # 3. kiri 서버 스크립트 생성 및 전송
        script_content = _get_kiria_server_script_content()
        remote_script_path = "/tmp/pk_service/pk_kiria_server.py"
        
        # 디렉토리 생성 명령 추가
        logger.info("원격 서버에 pk_service 디렉토리 생성 중...")
        controller.ensure_command_to_remote_target(
            cmd="mkdir -p /tmp/pk_service",
            timeout_seconds=10,
            use_sudo=False,
        )
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py', encoding='utf-8') as temp_f:
            temp_script_path = temp_f.name
            temp_f.write(script_content)
        
        try:
            logger.info("kiri 서버 스크립트를 Xavier에 전송 중...")
            ok = controller.ensure_file_transferred_to_remote_target(
                temp_script_path,
                remote_script_path,
            )
            
            if not ok:
                logger.error("스크립트 전송 실패")
                return False
            
            # 4. Xavier에서 kiri 서버 실행 (백그라운드)
            logger.info("Xavier에서 kiri 서버를 시작합니다...")
            logger.info("서버를 중지하려면 Xavier에서 Ctrl+C를 누르거나 프로세스를 종료하세요.")
            
            cmd = f"nohup python3 {remote_script_path} > /tmp/pk_service/pk_kiria_server.log 2>&1 &"
            stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
                cmd=cmd,
                timeout_seconds=10,
                use_sudo=False,
            )
            
            if exit_code == 0:
                logger.info("✅ kiri 서버가 Xavier에서 시작되었습니다.")
                if mic_available:
                    logger.info("✅ 마이크가 감지되어 음성 인식 기능을 사용할 수 있습니다.")
                else:
                    logger.info("⚠️ 마이크가 감지되지 않아 키보드 입력 모드로 동작합니다.")
                logger.info("서버 로그 확인: ssh로 Xavier 접속 후 'tail -f /tmp/pk_service/pk_kiria_server.log'")
                logger.info("서버 중지: Xavier에서 'pkill -f pk_kiria_server.py'")
                return True
            else:
                logger.error("kiri 서버 시작 실패")
                if stderr:
                    for line in stderr:
                        logger.error("  %s", line)
                return False
        
        finally:
            import os
            if os.path.exists(temp_script_path):
                try:
                    os.remove(temp_script_path)
                except Exception as e:
                    pass
        
    except Exception as e:
        logger.error(f"Xavier kiri 서버 시작 중 예외 발생: {e}", exc_info=True)
        return False



