def ensure_potplayer_started():
    """
        PotPlayer를 단일 인스턴스로 시작하는 함수
        이미 실행 중이면 새로 시작하지 않음
    """
    import subprocess

    import psutil

    import logging
    from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE


    try:
        # PotPlayer 프로세스 확인
        potplayer_running = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'PotPlayer' in proc.info['name']:
                    potplayer_running = True
                    logging.debug(f"PotPlayer가 이미 실행 중입니다 (PID: {proc.info['pid']})")
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        if not potplayer_running:
            # PotPlayer 시작
            cmd = f'"{F_POTPLAYER_EXE}"'
            logging.debug(f"PotPlayer를 시작합니다...")

            # 백그라운드에서 실행
            subprocess.Popen(cmd, shell=True)
            logging.debug(f"PotPlayer가 시작되었습니다")
        else:
            logging.debug(f"ℹ️ PotPlayer가 이미 실행 중입니다")

    except Exception as e:
        logging.debug(f"PotPlayer 시작 실패: {e}")
        raise Exception(f"PotPlayer 시작 실패: {e}")


def is_potplayer_running():
    """PotPlayer가 실행 중인지 확인"""
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'PotPlayer' in proc.info['name']:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    except Exception as e:
        return False


def get_potplayer_process():
    """실행 중인 PotPlayer 프로세스 정보 반환"""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                if 'PotPlayer' in proc.info['name']:
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return None
    except Exception as e:
        return None
