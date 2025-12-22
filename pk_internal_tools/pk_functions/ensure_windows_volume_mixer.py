from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


def _clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


@ensure_seconds_measured
def ensure_windows_volume_mixer():
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL


    # TODO 설치확인후 설치하는 코드
    # from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume

    """
    하드코딩된 설정으로 Windows 볼륨 믹서 제어
    - 마스터 볼륨 50%로 설정
    - chrome.exe 볼륨 30%로 설정
    """

    # --- 마스터 볼륨 50% ---
    speakers = AudioUtilities.GetSpeakers()
    interface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    endpoint = cast(interface, POINTER(IAudioEndpointVolume))
    endpoint.SetMasterVolumeLevelScalar(_clamp01(0.5), None)  # 50%

    # --- 크롬 볼륨 30% ---
    target = "chrome.exe"
    sessions = AudioUtilities.GetAllSessions()
    for s in sessions:
        if not s.Process:
            continue
        try:
            if s.Process.nick_name().lower() == target:
                vol = s._ctl.QueryInterface(ISimpleAudioVolume)
                vol.SetMasterVolume(_clamp01(0.3), None)  # 30%
                vol.SetMute(False, None)  # 음소거 해제
                print(f"[OK] {target} 볼륨을 30%로 설정 완료")
                break
        except Exception as e:
            print(f"[WARN] {target} 제어 중 오류: {e}")

    print("[DONE] 마스터 볼륨 50% 적용 완료")



