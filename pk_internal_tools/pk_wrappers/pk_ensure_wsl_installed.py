"""
간단한 WSL 확인 스크립트 (기존 모듈 의존성 없이)
"""
import subprocess
import sys
import os


def ensure_wsl_enabled_simple():
    """간단한 WSL 확인 테스트"""
    print("🔍 WSL 상태 확인 중...")
    print(PK_UNDERLINE)
    
    try:
        # n. WSL 명령어 실행 가능 여부 확인
        print("1️⃣ WSL 명령어 실행 가능 여부 확인...")
        result = subprocess.run(
            ['wsl', '--version'], 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            errors='ignore',
            timeout=10
        )
        if result.returncode == 0:
            print(f"✅ WSL 설치됨: {result.stdout.strip()}")
        else:
            print(f"❌ WSL 설치되지 않음: {result.stderr}")
            return False
        
        # n. 설치된 배포판 목록 확인 (바이너리로 읽고 디코딩)
        print("2️⃣ 설치된 배포판 목록 확인...")
        result = subprocess.run(
            ['wsl', '-l', '-v'], 
            capture_output=True, 
            timeout=10
        )
        if result.returncode == 0:
            # 바이너리 출력을 UTF-16으로 디코딩
            try:
                output = result.stdout.decode('utf-16-le')
            except UnicodeDecodeError:
                try:
                    output = result.stdout.decode('utf-16-be')
                except UnicodeDecodeError:
                    output = result.stdout.decode('utf-8', errors='ignore')
            
            print("✅ 설치된 배포판:")
            print(output)
            
            # Ubuntu 배포판 찾기
            if 'Ubuntu' in output:
                print("✅ Ubuntu 배포판 발견!")
                selected_distro = 'Ubuntu'
            else:
                print("❌ Ubuntu 배포판을 찾을 수 없습니다.")
                return False
            
            # n. Ubuntu 배포판으로 테스트
            print(f"\n3️⃣ {selected_distro} 배포판 테스트...")
            result = subprocess.run(
                ['wsl', '-d', selected_distro, '-e', 'bash', '-c', 'pwd'], 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                errors='ignore',
                timeout=10
            )
            if result.returncode == 0:
                print(f"✅ {selected_distro} 사용 가능: {result.stdout.strip()}")
            else:
                print(f"❌ {selected_distro} 사용 불가: {result.stderr}")
                return False
            
            # n. Docker 설치 확인
            print(f"\n4️⃣ Docker 설치 확인...")
            result = subprocess.run(
                ['wsl', '-d', selected_distro, '-e', 'bash', '-c', 'docker --version'], 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                errors='ignore',
                timeout=10
            )
            if result.returncode == 0:
                print(f"✅ Docker 설치됨: {result.stdout.strip()}")
            else:
                print(f"❌ Docker 설치되지 않음: {result.stderr}")
                return False
            
            # n. Docker Compose 설치 확인
            print(f"\n5️⃣ Docker Compose 설치 확인...")
            result = subprocess.run(
                ['wsl', '-d', selected_distro, '-e', 'bash', '-c', 'docker-compose --version'], 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                errors='ignore',
                timeout=10
            )
            if result.returncode == 0:
                print(f"✅ Docker Compose 설치됨: {result.stdout.strip()}")
            else:
                print(f"❌ Docker Compose 설치되지 않음: {result.stderr}")
                return False
            
            print("" + PK_UNDERLINE)
            print("✅ WSL 환경이 정상적으로 설정되어 있습니다!")
            return True
            
        else:
            print(f"❌ 배포판 목록 조회 실패: {result.stderr}")
            return False
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False


if __name__ == "__main__":
    success = ensure_wsl_enabled_simple()
    if success:
        print("✅ WSL 확인 성공!")
        sys.exit(0)
    else:
        print("❌ WSL 확인 실패!")
        sys.exit(1) 