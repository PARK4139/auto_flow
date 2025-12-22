import os


def ensure_powershell_environment_detected():
    """PowerShell 환경인지 확인합니다."""
    
    print("=" * 60)
    print(" PowerShell 환경 감지 디버깅 시작")
    print("=" * 60)
    
    # 방법 1: 환경 변수로 확인 (가장 신뢰할 수 있음)
    print("[DEBUG] 방법 1: 환경 변수 확인")
    if 'POWERSHELL_TELEMETRY_OPTOUT' in os.environ:
        print(" POWERSHELL_TELEMETRY_OPTOUT 환경변수 발견!")
        return True
    else:
        print(" POWERSHELL_TELEMETRY_OPTOUT 환경변수 없음")
    
    # 방법 2: PowerShell 관련 환경 변수 확인 (보조 수단)
    print("[DEBUG] 방법 2: PowerShell 관련 환경변수 확인 (보조 수단)")
    powershell_vars = [
        'POWERSHELL_TELEMETRY_OPTOUT',
        'PSModulePath',
        'PSExecutionPolicyPreference',
        'POWERSHELL_DISTRIBUTION_CHANNEL'
    ]
    
    found_vars = []
    for var in powershell_vars:
        if var in os.environ:
            found_vars.append(var)
            print(f" {var} 환경변수 발견!")
    
    if found_vars:
        print(f"️ PowerShell 관련 환경변수 {len(found_vars)}개 발견 (하지만 프로세스 체인 확인 필요)")
        print("️ 환경변수만으로는 정확하지 않을 수 있음 - 프로세스 체인 확인 우선")
    else:
        print(" PowerShell 관련 환경변수 없음")
    
    # 환경변수만으로는 판단하지 않고 프로세스 체인 확인을 우선
    
    # 방법 3: 프로세스 체인을 더 깊게 확인
    print("[DEBUG] 방법 3: 프로세스 체인 확인")
    try:
        import psutil
        current_process = psutil.Process()
        logging.debug(f" 현재 프로세스: {current_process.name()} (PID: {current_process.pid})")
        
        # 현재 프로세스가 python.exe인지 확인
        if current_process.name().lower() == 'python.exe':
            print(" 현재 프로세스는 python.exe")
            
            # 프로세스 체인을 최대 5단계까지 확인
            process_chain = []
            current = current_process
            
            for i in range(5):  # 최대 5단계
                try:
                    parent = current.parent()
                    if parent:
                        process_info = f"{i+1}단계: {parent.nick_name()} (PID: {parent.pid})"
                        process_chain.append(parent.nick_name().lower())
                        logging.debug(f" {process_info}")
                        current = parent
                    else:
                        logging.debug(f" {i+1}단계: 부모 프로세스 없음")
                        break
                except Exception as e:
                    logging.debug(f" {i+1}단계: 오류 발생 - {e}")
                    break
            
            print(f"\n[DEBUG] 프로세스 체인 요약: {' -> '.join(process_chain)}")
            
            # 프로세스 체인에 PowerShell이 있는지 확인
            for i, process_name in enumerate(process_chain):
                if any(name in process_name for name in ['powershell', 'pwsh']):
                    print(f" {i+1}단계에서 PowerShell 발견: {process_name}")
                    return True
                
                # cmd.exe가 있으면 확실히 PowerShell이 아님
                if 'cmd.exe' in process_name:
                    print(f" {i+1}단계에서 cmd.exe 발견: {process_name} (PowerShell 아님)")
                    return False
                
                # explorer.exe나 다른 GUI 프로세스는 중단
                if process_name in ['explorer.exe', 'conhost.exe']:
                    print(f" {i+1}단계에서 GUI 프로세스 발견: {process_name} (체인 중단)")
                    break
        else:
            print(f" 현재 프로세스는 python.exe가 아님: {current_process.name()}")
    except Exception as e:
        print(f" 프로세스 체인 확인 중 오류: {e}")
    
    # 방법 4: 추가 디버그 정보
    print("[DEBUG] 방법 4: 추가 정보")
    logging.debug(f" 전체 환경변수 개수: {len(os.environ)}")
    
    # PowerShell 관련 환경변수만 필터링
    ps_related_vars = [k for k in os.environ.keys() if 'power' in k.lower() or 'ps' in k.lower()]
    logging.debug(f" PowerShell 관련 환경변수: {ps_related_vars}")
    
    # 현재 작업 디렉토리 확인
    logging.debug(f" 현재 작업 디렉토리: {os.getcwd()}")
    
    print("" + "=" * 60)
    print(" PowerShell 환경 감지 결과: FALSE")
    print("=" * 60)
    
    return False
