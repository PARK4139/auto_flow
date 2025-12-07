
import asyncio
import sys
import logging
import json
import dataclasses
from datetime import datetime, date
from tapo import ApiClient

def format_runtime_seconds(seconds):
    """초 단위 시간을 읽기 쉬운 형식으로 변환"""
    if seconds is None or seconds == 0:
        return "0초"
    runtime_min = seconds // 60
    runtime_hour = runtime_min // 60
    if runtime_hour > 0:
        return str(runtime_hour) + "시간 " + str(runtime_min % 60) + "분 (" + str(seconds) + "초)"
    elif runtime_min > 0:
        return str(runtime_min) + "분 (" + str(seconds) + "초)"
    else:
        return str(seconds) + "초"

def json_serializer(obj):
    """JSON 직렬화를 위한 커스텀 함수"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    obj_type = type(obj)
    raise TypeError("Type " + str(obj_type) + " not serializable")

# ANSI 색상 코드 (노란색)
YELLOW = "\033[33m"
RESET = "\033[0m"

def get_text_yellow(text):
    """텍스트를 노란색으로 변환"""
    return f"{YELLOW}{text}{RESET}"

def print_section_header(title, width=60, output_file=sys.stderr):
    """섹션 헤더 출력 (노란색)"""
    print("", file=output_file)
    print(get_text_yellow("=" * width), file=output_file)
    print(get_text_yellow(title), file=output_file)

def print_section_footer(width=60, output_file=sys.stderr):
    """섹션 푸터 출력 (노란색)"""
    print(get_text_yellow("=" * width), file=output_file)

def print_subsection_header(title, width=60, output_file=sys.stderr):
    """서브섹션 헤더 출력 (노란색)"""
    print("", file=output_file)
    print(get_text_yellow(title), file=output_file)
    print(get_text_yellow("-" * width), file=output_file)

def print_subsection_footer(width=60, output_file=sys.stderr):
    """서브섹션 푸터 출력 (노란색)"""
    print(get_text_yellow("-" * width), file=output_file)

def print_key_value(key, value, indent=2, output_file=sys.stderr):
    """키-값 쌍 출력 (노란색)"""
    indent_str = " " * indent
    print(get_text_yellow(indent_str + key + ": " + str(value)), file=output_file)

def print_structured_data(data, title="데이터", summary_title="주요 정보 요약", output_file=sys.stderr, show_json=True, show_summary=True):
    """구조화된 데이터 출력 (노란색)"""
    if isinstance(data, dict):
        if show_json:
            print_section_header(title, output_file=output_file)
            json_str = get_pretty_json_string(data)
            print(get_text_yellow(json_str), file=output_file)
            print_section_footer(output_file=output_file)
        
        if show_summary:
            # Summary 내용을 문자열로 병합
            summary_lines = []
            separator = "_" * 40
            
            # 1. 기본 상태 정보
            summary_lines.append("")
            summary_lines.append(separator)
            summary_lines.append("# 기본 상태")
            summary_lines.append("")
            if "device_on" in data:
                status = "ON" if data["device_on"] else "OFF"
                status_color = "🟢" if data["device_on"] else "🔴"
                summary_lines.append(f"{status_color} 전원 상태: {status}")
            if "on_time" in data:
                runtime = format_runtime_seconds(data["on_time"])
                summary_lines.append(f"⏱️  켜져 있던 시간: {runtime}")
            if "local_time" in data:
                summary_lines.append(f"🕐 조회 시간: {data['local_time']}")
            summary_lines.append("")
            
            # 2. 에너지 정보 (있을 경우)
            energy_fields = ["current_power", "today_energy", "month_energy", "today_runtime", "month_runtime"]
            if any(field in data for field in energy_fields):
                summary_lines.append(separator)
                summary_lines.append("# 에너지 정보")
                summary_lines.append("")
                if "current_power" in data:
                    power = data["current_power"]
                    summary_lines.append(f"⚡ 현재 소비 전력: {power} W")
                if "today_energy" in data:
                    summary_lines.append(f"📊 오늘 사용 에너지: {data['today_energy']} Wh")
                if "month_energy" in data:
                    summary_lines.append(f"📈 이번 달 사용 에너지: {data['month_energy']} Wh")
                if "today_runtime" in data:
                    runtime = format_runtime_seconds(data["today_runtime"])
                    summary_lines.append(f"⏱️  오늘 가동 시간: {runtime}")
                if "month_runtime" in data:
                    runtime = format_runtime_seconds(data["month_runtime"])
                    summary_lines.append(f"⏱️  이번 달 가동 시간: {runtime}")
            
            # 3. 장치 정보
            summary_lines.append(separator)
            summary_lines.append("# 장치 정보")
            summary_lines.append("")
            if "model" in data:
                model = data["model"]
            elif "device_model" in data:
                model = data["device_model"]
            else:
                model = None
            if model:
                summary_lines.append(f"🔌 장치 모델: {model}")
            if "fw_ver" in data:
                summary_lines.append(f"📦 펌웨어 버전: {data['fw_ver']}")
            if "hw_ver" in data:
                summary_lines.append(f"🔧 하드웨어 버전: {data['hw_ver']}")
            if "device_id" in data:
                device_id = data["device_id"]
                # 긴 ID는 축약하여 표시
                if len(device_id) > 16:
                    device_id_short = device_id[:8] + "..." + device_id[-8:]
                    summary_lines.append(f"🆔 장치 ID: {device_id_short}")
                else:
                    summary_lines.append(f"🆔 장치 ID: {device_id}")
            summary_lines.append("")
            
            # 4. 네트워크 정보
            summary_lines.append(separator)
            summary_lines.append("# 네트워크 정보")
            summary_lines.append("")
            if "ip" in data:
                summary_lines.append(f"🌐 IP 주소: {data['ip']}")
            if "mac" in data:
                summary_lines.append(f"🔗 MAC 주소: {data['mac']}")
            if "rssi" in data:
                rssi = data["rssi"]
                # RSSI를 신호 품질로 변환
                if rssi >= -50:
                    quality = "우수"
                elif rssi >= -60:
                    quality = "양호"
                elif rssi >= -70:
                    quality = "보통"
                else:
                    quality = "약함"
                summary_lines.append(f"📶 신호 강도: {rssi} dBm ({quality})")
            elif "signal_level" in data:
                level = data["signal_level"]
                levels = {1: "약함", 2: "보통", 3: "양호", 4: "우수"}
                quality = levels.get(level, "알 수 없음")
                summary_lines.append(f"📶 신호 레벨: {level}/4 ({quality})")
            summary_lines.append("")
            
            # 전체 Summary를 하나의 문자열로 병합하여 한 번에 노란색으로 출력
            summary_text = "\n".join(summary_lines)
            print(get_text_yellow(summary_text), file=output_file)

def get_pretty_json_string(data):
    """
    주어진 파이썬 객체(dataclass 포함)를 가독성 좋은 JSON 문자열로 변환합니다.
    - ensure_ascii=False: 한글이 깨지지 않도록 보장합니다.
    - indent=4: 4칸 들여쓰기로 가독성을 높입니다.
    - datetime 객체는 ISO 형식 문자열로 변환합니다.
    """
    try:
        if dataclasses.is_dataclass(data):
            data_to_dump = dataclasses.asdict(data)
        elif isinstance(data, dict):
            data_to_dump = data
        else:
            # 일반 객체의 경우 속성을 추출
            data_to_dump = dict()
            for attr in dir(data):
                if not attr.startswith('_'):
                    try:
                        attr_value = getattr(data, attr)
                        if not callable(attr_value):
                            data_to_dump[attr] = attr_value
                    except Exception:
                        pass
        
        return json.dumps(data_to_dump, ensure_ascii=False, indent=2, default=json_serializer)
    except Exception as e:
        return json.dumps({"error": "JSON serialization failed", "message": str(e)}, ensure_ascii=False, indent=4)

# 로깅 설정 (INFO 레벨로 변경하여 디버그 메시지 감소)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    stream=sys.stderr
)

async def control_p110m():
    import sys as sys_module  # 모듈 레벨의 sys를 명시적으로 import
    
    host = {HOST_ESCAPED}
    username = {USERNAME_ESCAPED}
    password = {PASSWORD_ESCAPED}
    action = {ACTION_ESCAPED}
    
    # ApiClient 초기화 과정 로깅
    try:
        client = ApiClient(username, password)
    except Exception as e:
        print(f"❌ ApiClient 초기화 실패: {e}", file=sys_module.stderr)
        print(f"   오류 타입: {type(e).__name__}", file=sys_module.stderr)
        import traceback
        print("   상세 스택:", file=sys_module.stderr)
        for line in traceback.format_exc().split('\n'):
            print(f"   {line}", file=sys_module.stderr)
        raise
    
    # P110M 장치 연결
    try:
        device = await client.p110(host)
    except Exception as e:
        print(f"❌ P110M 장치 연결 실패: {e}", file=sys_module.stderr)
        print(f"   오류 타입: {type(e).__name__}", file=sys_module.stderr)
        error_str = str(e)
        
        # 해시 불일치 오류 상세 분석
        if "hash" in error_str.lower() or "InvalidCredentials" in error_str:
            print("", file=sys_module.stderr)
            print("=" * 60, file=sys_module.stderr)
            print("해시 불일치 오류 상세 분석", file=sys_module.stderr)
            print("=" * 60, file=sys_module.stderr)
            print(f"전체 오류 메시지: {error_str}", file=sys_module.stderr)
            print("", file=sys_module.stderr)
            print("가능한 원인 분석:", file=sys_module.stderr)
            print("  1. ⚠️  Username 형식 문제:", file=sys_module.stderr)
            print("     - Username이 전화번호인 경우, Tapo는 이메일을 요구할 수 있습니다.", file=sys_module.stderr)
            print("     - Tapo 앱에서 사용하는 로그인 방식을 확인하세요.", file=sys_module.stderr)
            print("     - 이메일로 로그인하는 경우: 이메일 주소를 사용하세요.", file=sys_module.stderr)
            print("  2. Klap 프로토콜 handshake 해시 불일치:", file=sys_module.stderr)
            print("     - Klap 프로토콜의 handshake1 단계에서 해시 계산 실패", file=sys_module.stderr)
            print("     - 비밀번호 해싱 방식이 서버와 일치하지 않을 수 있습니다.", file=sys_module.stderr)
            print("  3. Tapo 서버의 인증 프로토콜이 변경되었을 수 있습니다.", file=sys_module.stderr)
            print("  4. 라이브러리 버전이 Tapo 서버와 호환되지 않을 수 있습니다.", file=sys_module.stderr)
            print("  5. 2FA가 활성화되어 있어 로컬 API 인증이 실패할 수 있습니다.", file=sys_module.stderr)
            print("     - tapo 라이브러리는 2FA를 지원하지 않을 수 있습니다.", file=sys_module.stderr)
            print("     - 해결: Home Assistant 또는 python-kasa 사용 권장", file=sys_module.stderr)
            print("", file=sys_module.stderr)
            print("해결 방법 시도 (우선순위 순):", file=sys_module.stderr)
            print("  1. ⭐ Username 확인 (가장 중요):", file=sys_module.stderr)
            print("     - Tapo 앱을 열고 로그인 방식을 확인하세요.", file=sys_module.stderr)
            print("     - 이메일로 로그인하는 경우: TAPO_USERNAME을 이메일 주소로 변경하세요.", file=sys_module.stderr)
            print("     - 예: TAPO_USERNAME=your-email@example.com", file=sys_module.stderr)
            print("  2. tapo 라이브러리 최신 버전으로 업데이트:", file=sys_module.stderr)
            print("     pip install --upgrade tapo", file=sys_module.stderr)
            print("     또는:", file=sys_module.stderr)
            print("     pip install --upgrade python-tapo", file=sys_module.stderr)
            print("  3. 다른 인증 방식 시도 (로컬 제어):", file=sys_module.stderr)
            print("     - python-kasa 라이브러리 사용 (계정 불필요)", file=sys_module.stderr)
            print("  4. Home Assistant 통합 사용 (가장 안정적):", file=sys_module.stderr)
            print("     - Home Assistant는 Tapo 통합을 통해 더 안정적으로 작동합니다.", file=sys_module.stderr)
            print("=" * 60, file=sys_module.stderr)
        
        import traceback
        print("   상세 스택:", file=sys_module.stderr)
        for line in traceback.format_exc().split('\n'):
            print(f"   {line}", file=sys_module.stderr)
        raise
    
    try:
        if action == "on":
            print("P110M 켜기 시도 중...", file=sys_module.stderr)
            await device.on()
            print("✅ P110M 켜기 성공")
        elif action == "off":
            print("P110M 끄기 시도 중...", file=sys_module.stderr)
            await device.off()
            print("✅ P110M 끄기 성공")
        elif action == "toggle":
            print("P110M 상태 확인 중...", file=sys_module.stderr)
            current_state = None
            
            # 방법 1: get_device_info_json() 시도 (가장 안정적, JSON으로 직접 파싱)
            try:
                import json
                device_info_json = await device.get_device_info_json()
                current_state = device_info_json.get("device_on", None)
                if current_state is not None:
                    print(f"✅ 현재 상태 확인 (get_device_info_json): {'ON' if current_state else 'OFF'}", file=sys_module.stderr)
            except Exception as e:
                print(f"⚠️ get_device_info_json() 실패: {e}", file=sys_module.stderr)
                print("get_device_info()로 시도 중...", file=sys_module.stderr)
                # 방법 2: get_device_info() 시도 (fallback)
                try:
                    device_info = await device.get_device_info()
                    current_state = getattr(device_info, 'device_on', None)
                    if current_state is not None:
                        print(f"✅ 현재 상태 확인 (get_device_info): {'ON' if current_state else 'OFF'}", file=sys_module.stderr)
                except Exception as e2:
                    print(f"⚠️ get_device_info()도 실패: {e2}", file=sys_module.stderr)
            
            # toggle은 현재 상태를 반드시 알아야 함
            if current_state is None:
                print("", file=sys_module.stderr)
                print("=" * 60, file=sys_module.stderr)
                print("❌ Toggle 실패: 상태를 확인할 수 없습니다", file=sys_module.stderr)
                print("=" * 60, file=sys_module.stderr)
                print("Toggle 기능은 현재 상태(ON/OFF)를 반드시 알아야 합니다:", file=sys_module.stderr)
                print("  - 현재 ON이면 -> OFF로", file=sys_module.stderr)
                print("  - 현재 OFF이면 -> ON으로", file=sys_module.stderr)
                print("", file=sys_module.stderr)
                print("문제:", file=sys_module.stderr)
                print("  - get_device_info_json() 및 get_device_info() 모두 실패", file=sys_module.stderr)
                print("  - tapo 라이브러리가 P110M의 응답을 파싱하지 못함", file=sys_module.stderr)
                print("", file=sys_module.stderr)
                print("해결 방법:", file=sys_module.stderr)
                print("  1. 'on' 또는 'off' 액션을 직접 사용하세요:", file=sys_module.stderr)
                print("     - 현재 상태를 알 필요 없이 직접 제어 가능", file=sys_module.stderr)
                print("  2. Home Assistant를 통한 제어 사용:", file=sys_module.stderr)
                print("     - Home Assistant는 상태 확인이 정상 작동합니다", file=sys_module.stderr)
                print("     - 'P110M control via Home Assistant' 작업 사용", file=sys_module.stderr)
                print("  3. tapo 라이브러리 업데이트 시도:", file=sys_module.stderr)
                print("     - pip install --upgrade tapo", file=sys_module.stderr)
                print("=" * 60, file=sys_module.stderr)
                print("", file=sys_module.stderr)
                raise Exception("Toggle requires current state, but state check failed")
            else:
                # 상태 확인 성공: 정상 toggle
                if current_state:
                    print("P110M 끄기 시도 중 (toggle: ON -> OFF)...", file=sys_module.stderr)
                    await device.off()
                    print("✅ P110M 끄기 완료 (toggle)")
                else:
                    print("P110M 켜기 시도 중 (toggle: OFF -> ON)...", file=sys_module.stderr)
                    await device.on()
                    print("✅ P110M 켜기 완료 (toggle)")
        elif action == "info":
            print("P110M 정보 조회 중...")
            print("")

            # 장치 정보 조회
            device_info_json = None
            try:
                device_info_json = await device.get_device_info_json()
                # 성공 메시지는 생략 (Summary에서 확인 가능)
            except Exception as e:
                print(f"⚠️ get_device_info_json() 실패: {e}", file=sys_module.stderr)
                print("get_device_info()로 시도 중...", file=sys_module.stderr)
                try:
                    device_info = await device.get_device_info()
                    # device_info 객체를 dict로 변환
                    device_info_json = dict()
                    for attr in dir(device_info):
                        if not attr.startswith('_'):
                            try:
                                value = getattr(device_info, attr)
                                if not callable(value):
                                    device_info_json[attr] = value
                            except Exception:
                                pass
                    print("✅ 장치 정보 조회 성공 (get_device_info)", file=sys_module.stderr)
                except Exception as e2:
                    print(f"❌ 장치 정보 조회 실패: {e2}", file=sys_module.stderr)
                    device_info_json = None
            
            # 에너지 데이터 조회
            energy_dict = None
            try:
                energy_data = None
                if hasattr(device, 'get_energy_usage'):
                    energy_data = await device.get_energy_usage()
                elif hasattr(device, 'get_energy'):
                    energy_data = await device.get_energy()
                else:
                    print("⚠️ 에너지 데이터 조회 메서드를 찾을 수 없습니다.", file=sys_module.stderr)
                
                if energy_data is not None:
                    # 성공 메시지는 생략 (Summary에서 확인 가능)
                    # EnergyUsageResult 객체를 dict로 변환
                    try:
                        if isinstance(energy_data, dict):
                            energy_dict = energy_data
                        elif hasattr(energy_data, '__dict__'):
                            energy_dict = energy_data.__dict__
                        else:
                            # 객체의 속성을 직접 추출
                            energy_dict = dict()
                            for attr in dir(energy_data):
                                if not attr.startswith('_'):
                                    try:
                                        attr_value = getattr(energy_data, attr)
                                        if not callable(attr_value):
                                            energy_dict[attr] = attr_value
                                    except Exception:
                                        pass
                    except Exception as convert_error:
                        print(f"⚠️ 에너지 객체 변환 중 오류: {convert_error}", file=sys_module.stderr)
                        energy_dict = {"raw_data": str(energy_data), "error": str(convert_error)}
            except Exception as e:
                print(f"⚠️ 에너지 데이터 조회 실패: {e}", file=sys_module.stderr)
            
            # 장치 정보와 에너지 데이터 통합
            merged_data = dict()
            if device_info_json:
                merged_data.update(device_info_json)
            if energy_dict:
                merged_data.update(energy_dict)
            
            if merged_data:
                # JSON과 Summary 모두 출력 (JSON은 원본 그대로, Summary는 정리된 형태)
                print_structured_data(
                    merged_data,
                    title="# P110M 전체 정보 및 에너지 데이터 (JSON)",
                    summary_title="주요 정보 요약",
                    output_file=sys_module.stderr,
                    show_json=True,  # JSON은 그대로 출력
                    show_summary=True  # Summary는 정리된 형태로 출력
                )
                
                # 에너지 데이터가 있는 경우 DB에 저장
                if energy_dict:
                    try:
                        import sys
                        import os
                        from pathlib import Path
                        
                        # Xavier의 DB 경로 설정 (Linux 경로)
                        db_dir = Path.home() / "pk_system" / ".pk_system"
                        db_dir.mkdir(parents=True, exist_ok=True)
                        db_path = db_dir / "pk_system.sqlite"
                        
                        # DB 저장 함수 (Xavier에서 직접 실행)
                        import sqlite3
                        from datetime import datetime
                        
                        # 테이블 생성
                        conn = sqlite3.connect(str(db_path))
                        cur = conn.cursor()
                        cur.execute("""
                            CREATE TABLE IF NOT EXISTS p110m_energy_data (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                device_host TEXT NOT NULL,
                                current_power REAL,
                                today_energy REAL,
                                today_runtime INTEGER,
                                month_energy REAL,
                                month_runtime INTEGER,
                                local_time TIMESTAMP,
                                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        """)
                        cur.execute("""
                            CREATE INDEX IF NOT EXISTS idx_p110m_energy_collected_at 
                            ON p110m_energy_data(collected_at DESC)
                        """)
                        cur.execute("""
                            CREATE INDEX IF NOT EXISTS idx_p110m_energy_device_host 
                            ON p110m_energy_data(device_host)
                        """)
                        
                        # local_time 처리
                        local_time = energy_dict.get("local_time")
                        if local_time is not None:
                            if isinstance(local_time, datetime):
                                local_time_str = local_time.isoformat()
                            elif isinstance(local_time, str):
                                local_time_str = local_time
                            else:
                                local_time_str = str(local_time)
                        else:
                            local_time_str = None
                        
                        # 데이터 저장
                        cur.execute("""
                            INSERT INTO p110m_energy_data 
                            (device_host, current_power, today_energy, today_runtime, 
                             month_energy, month_runtime, local_time, collected_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            {HOST_ESCAPED},
                            energy_dict.get("current_power"),
                            energy_dict.get("today_energy"),
                            energy_dict.get("today_runtime"),
                            energy_dict.get("month_energy"),
                            energy_dict.get("month_runtime"),
                            local_time_str,
                            datetime.now().isoformat()
                        ))
                        
                        conn.commit()
                        conn.close()
                        
                        # DB 저장 메시지는 생략 (조용히 저장)
                    except Exception as db_err:
                        print(f"⚠️ DB 저장 실패: {db_err}", file=sys_module.stderr)
                        import traceback
                        traceback.print_exc(file=sys_module.stderr)
            else:
                print("⚠️ 조회된 데이터가 없습니다.", file=sys_module.stderr)
            
            # info 액션 완료 (호스트 머신에서 input 처리)
            print("", file=sys_module.stderr)
            print("=" * 60, file=sys_module.stderr)
        else:
            print(f"❌ 지원하지 않는 액션: {action}", file=sys_module.stderr)
            sys_module.exit(1)
        
        sys_module.exit(0)
    except Exception as e:
        error_str = str(e)
        error_type = type(e).__name__
        
        print("", file=sys_module.stderr)
        print("=" * 60, file=sys_module.stderr)
        print("❌ 오류 발생", file=sys_module.stderr)
        print("=" * 60, file=sys_module.stderr)
        print(f"오류 타입: {error_type}", file=sys_module.stderr)
        print(f"오류 메시지: {error_str}", file=sys_module.stderr)
        
        # 전체 스택 트레이스 출력
        import traceback
        print("", file=sys_module.stderr)
        print("상세 스택 트레이스:", file=sys_module.stderr)
        print("-" * 60, file=sys_module.stderr)
        for line in traceback.format_exc().split('\n'):
            if line.strip():
                print(f"  {line}", file=sys_module.stderr)
        print("-" * 60, file=sys_module.stderr)
        
        # 인증 오류인 경우 상세 정보 제공
        if "InvalidCredentials" in error_str or "hash" in error_str.lower():
            print("", file=sys_module.stderr)
            print("=" * 60, file=sys_module.stderr)
            print("Tapo 인증 실패", file=sys_module.stderr)
            print("=" * 60, file=sys_module.stderr)
            print("가능한 원인:", file=sys_module.stderr)
            print("  1. Tapo 계정 이메일 또는 비밀번호가 잘못되었습니다.", file=sys_module.stderr)
            print("  2. Tapo 계정이 2단계 인증(2FA)을 사용하는 경우:", file=sys_module.stderr)
            print("     - tapo 라이브러리는 2FA가 활성화된 계정을 지원하지 않을 수 있습니다.", file=sys_module.stderr)
            print("     - 해결 방법:", file=sys_module.stderr)
            print("       ① 2FA 일시적으로 비활성화 (보안 약화):", file=sys_module.stderr)
            print("          - Tapo 앱 > 나 > 계정 아이콘 > 로그인 보안 > 2단계 인증 > 비활성화", file=sys_module.stderr)
            print("       ② Home Assistant 사용 (권장):", file=sys_module.stderr)
            print("          - Home Assistant의 Tapo 통합은 2FA를 지원할 수 있습니다.", file=sys_module.stderr)
            print("          - 'P110M control via Home Assistant' 작업 사용", file=sys_module.stderr)
            print("       ③ python-kasa 라이브러리 사용 (로컬 제어, 계정 불필요):", file=sys_module.stderr)
            print("          - 계정 인증이 필요 없으므로 2FA 문제가 없습니다.", file=sys_module.stderr)
            print("          - 'P110M control via Tapo Local API (python-kasa)' 작업 사용", file=sys_module.stderr)
            print("  3. Tapo 서버의 인증 프로토콜이 변경되었을 수 있습니다.", file=sys_module.stderr)
            print("  4. tapo 라이브러리 버전 문제일 수 있습니다.", file=sys_module.stderr)
            print("", file=sys_module.stderr)
            print("해결 방법 (권장 순서):", file=sys_module.stderr)
            print("  1. Tapo 앱에서 직접 로그인 테스트:", file=sys_module.stderr)
            print("     - Tapo 앱을 열고 동일한 계정으로 로그인해보세요.", file=sys_module.stderr)
            print("     - 로그인이 성공하면, 비밀번호를 다시 확인하세요.", file=sys_module.stderr)
            print("  2. 환경 변수 확인:", file=sys_module.stderr)
            print("     - TAPO_USERNAME: Tapo 계정 이메일 확인", file=sys_module.stderr)
            print("     - TAPO_PW: Tapo 계정 비밀번호 확인", file=sys_module.stderr)
            print("     - 공백이나 특수문자가 올바르게 입력되었는지 확인하세요.", file=sys_module.stderr)
            print("  3. ⭐ Home Assistant를 통한 제어 사용 (가장 안정적):", file=sys_module.stderr)
            print("     - 'P110M control via Home Assistant' 작업 사용", file=sys_module.stderr)
            print("     - Home Assistant는 Tapo 통합을 통해 더 안정적으로 작동합니다.", file=sys_module.stderr)
            print("  4. python-kasa 라이브러리 시도 (로컬 제어, 계정 불필요):", file=sys_module.stderr)
            print("     - 'P110M control via Tapo Local API (python-kasa)' 작업 사용", file=sys_module.stderr)
            print("     - 단, python-kasa는 Tapo 장치를 완전히 지원하지 않을 수 있습니다.", file=sys_module.stderr)
            print("=" * 60, file=sys_module.stderr)
        
        sys_module.exit(1)

if __name__ == "__main__":
    asyncio.run(control_p110m())
