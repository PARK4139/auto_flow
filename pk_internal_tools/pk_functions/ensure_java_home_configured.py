import os
import platform
import logging

def ensure_java_home_configured() -> bool:
    """
    JAVA_HOME 환경 변수가 설정되어 있고 유효한지 확인합니다.
    설정되지 않은 경우, 일반적인 설치 경로에서 Java를 찾아 현재 프로세스에 대해 환경 변수를 설정합니다.

    Returns:
        bool: JAVA_HOME이 성공적으로 설정되었으면 True, 아니면 False.
    """
    # n. JAVA_HOME이 이미 올바르게 설정되었는지 확인
    java_home = os.environ.get('JAVA_HOME')
    if java_home:
        # java.exe 또는 java 바이너리가 있는지 확인하여 경로 유효성 검사
        java_executable = 'java.exe' if platform.system() == 'Windows' else 'java'
        if os.path.exists(os.path.join(java_home, 'bin', java_executable)):
            logging.info(f"JAVA_HOME is already set and valid: {java_home}")
            return True

    # n. Windows가 아닌 경우, 자동 감지 지원 안 함을 알림
    if platform.system() != 'Windows':
        logging.warning("Automatic JAVA_HOME detection is currently only supported on Windows.")
        logging.warning("Please set the JAVA_HOME environment variable manually.")
        return False

    # n. Windows의 경우, 일반적인 경로에서 Java 설치 위치 탐색
    logging.info("JAVA_HOME not set or invalid. Searching for Java installations...")
    search_paths = [
        os.environ.get("ProgramFiles", "C:\\Program Files"),
        os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
    ]

    potential_homes = []
    for path in search_paths:
        java_path = os.path.join(path, "Java")
        if os.path.isdir(java_path):
            for dirname in os.listdir(java_path):
                dirpath = os.path.join(java_path, dirname)
                if os.path.isdir(dirpath) and os.path.exists(os.path.join(dirpath, 'bin', 'java.exe')):
                    potential_homes.append(dirpath)

    if not potential_homes:
        # n. Java 설치를 찾지 못한 경우, 사용자에게 안내
        logging.error("--- Java Installation Not Found ---")
        logging.error("KoNLPy requires a Java installation to function.")
        logging.error("Please install a Java JDK (version 8 or higher) and try again.")
        logging.error("Recommended Download: https://www.oracle.com/java/technologies/downloads/")
        return False

    # n. 찾은 경로 중 가장 적합한 것을 선택 (JDK 우선, 최신 버전 우선)
    potential_homes.sort(key=lambda p: ('jdk' not in p.lower(), p), reverse=True)
    best_path = potential_homes[0]

    # 6. 현재 프로세스에 대해 JAVA_HOME 설정
    logging.info(f"Found Java at: {best_path}. Setting JAVA_HOME for the current session.")
    os.environ['JAVA_HOME'] = best_path
    return True

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    print("Checking for Java configuration...")
    is_configured = ensure_java_home_configured()
    if is_configured:
        print(f"\nJava is configured correctly. JAVA_HOME: {os.environ['JAVA_HOME']}")
    else:
        print("Java configuration check failed. Please see the log messages above.")
