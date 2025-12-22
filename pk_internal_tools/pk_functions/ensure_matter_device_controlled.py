#!/usr/bin/env python3

"""
All-in-one Matter control (Native BLE commissioning, uv/.venv aware)
- Single file, lazy imports, no Docker fallback.
- Always run python-matter-server on Python 3.12. If current Python != 3.12,
  create/use .venv_matter via `uv venv --python 3.12 .venv_matter`.
- Auto-install CHIP layer & python-matter-server into that 3.12 interpreter.
- Auto-install bleak into your *current* controller env when missing.
- All error cases are logged as logging.warning with detailed diagnostics.

Call style:
    asyncio.run(ensure_matter_smart_controllable())
"""

from __future__ import annotations

import asyncio
import glob
import logging
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import time
from contextlib import suppress
from shutil import which
from typing import Any, Dict, List, Optional, Tuple

from pk_internal_tools.pk_functions.ensure_sensitive_info_masked import ensure_sensitive_info_masked
# ===== Optional decorator fallback (must be defined before use) ======================
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


# ------------------------------------------------------------------------------------
# NOTE: 프로젝트 전역에서 로깅 레벨/핸들러를 이미 구성한다고 하셔서 여기선 기본설정 안함.
#       모든 실패/에러는 logging.warning으로 상세 로그를 남기도록 변경.
# ------------------------------------------------------------------------------------


def _parse_node_id_maybe(s: str) -> Optional[int]:
    s = (s or "").strip().lower()
    try:
        return int(s, 16) if s.startswith("0x") else int(s, 10)
    except Exception as e:
        return None


# ===== Subprocess helpers (UTF-8 enforced) ===========================================
_HA_SIMPLE = "https://pip.home-assistant.io/simple"
_NET_DIAG_ONCE = {"done": False}


def _merge_env(env_extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUTF8", "1")
    if env_extra:
        env.update(env_extra)
    return env


def _run_ex(
        cmd: List[str],
        timeout: Optional[int] = None,
        env_extra: Optional[Dict[str, str]] = None,
) -> Tuple[bool, int, str, str]:
    """subprocess.run with UTF-8 decode and optional env merge (prevents cp949 decode crashes)."""
    env = _merge_env(env_extra)
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
    except TypeError:
        # Older Python without 'encoding' kw (safety)
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False, env=env)
    return (p.returncode == 0), p.returncode, (p.stdout or ""), (p.stderr or "")


def _run(cmd: List[str], *, timeout: Optional[int] = None, env_extra: Optional[Dict[str, str]] = None) -> Tuple[bool, str]:
    ok, rc, so, se = _run_ex(cmd, timeout=timeout, env_extra=env_extra)
    return ok, (so + se).strip()


def _dns_ok(host: str) -> bool:
    try:
        socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
        return True
    except Exception as e:
        logging.warning("DNS 조회 실패: host=%s err=%s", host, e)
        return False


def _winhttp_proxy_env_if_needed() -> Dict[str, str]:
    """Windows WinHTTP 프록시 설정을 가져와 PIP/uv 용 HTTPS_PROXY로 전달."""
    if platform.system().lower() != "windows":
        return {}
    ok, rc, so, se = _run_ex(["netsh", "winhttp", "show", "proxy"])
    if not ok:
        return {}
    s = (so or se or "")
    if "Direct access (no proxy)" in s or "직접 액세스" in s:
        return {}
    m = re.search(r"Proxy Server\s*:\s*(\S+)", s)
    if not m:
        return {}
    proxy = m.group(1)
    https = None
    for part in proxy.split(";"):
        part = part.strip()
        if part.lower().startswith("https="):
            https = part.split("=", 1)[1]
            break
    https = https or proxy.split(";", 1)[0].split("=", 1)[-1]
    return {"HTTPS_PROXY": f"http://{https}", "HTTP_PROXY": f"http://{https}"} if https else {}


def _auto_wheels_hint_dir(_: List[str]) -> Optional[str]:
    """오프라인 휠 기본 탐색 경로."""
    for cand in [
        os.environ.get("MATTER_WHEELS_DIR"),
        os.path.join(os.getcwd(), "wheels"),
        os.path.join(os.getcwd(), "vendor", "wheels"),
        os.path.join(os.path.expanduser("~"), "Downloads", "matter_wheels"),
    ]:
        if cand and os.path.isdir(cand):
            return cand
    return None


def _glob_wheels(dirpath: str) -> List[str]:
    pats = [
        "home_assistant_chip_core-*-cp312-*-win_amd64.whl",
        "home_assistant_chip_clusters-*-cp312-*-win_amd64.whl",
    ]
    files: List[str] = []
    for p in pats:
        files += glob.glob(os.path.join(dirpath, p))
    return sorted(files)


def _log_offline_wheels_state(dirpath: Optional[str]) -> None:
    if not dirpath:
        logging.warning(
            "오프라인 휠 경로를 찾지 못했습니다. MATTER_WHEELS_DIR 또는 .\\wheels 사용 가능.")
        return
    files = _glob_wheels(dirpath)
    if files:
        logging.info("오프라인 휠 발견(%s):\n  %s", dirpath, "\n  ".join(files[-6:]))
    else:
        logging.warning(
            "오프라인 휠이 %s 에 없습니다. 아래 2개가 필요:\n"
            "  home_assistant_chip_core-*-cp312-*-win_amd64.whl\n"
            "  home_assistant_chip_clusters-*-cp312-*-win_amd64.whl",
            dirpath,
        )


def _should_offline_only() -> bool:
    """환경변수 또는 DNS 실패 시 네트워크 시도를 생략."""
    if os.getenv("MATTER_OFFLINE_ONLY") == "1":
        return True
    # HA 인덱스가 해석 안 되면 사실상 오프라인과 동일
    return not _dns_ok("pip.home-assistant.io")


def _uv_cmd(pyver: Optional[str], pip_args: List[str]) -> List[str]:
    """
    uv pip 호출. 구버전 호환 위해 두 가지 스타일을 모두 시도.
    - 우선: 특정 파이썬 버전 붙여 실행 (uv pip -p 3.12 install -- ...)
    - 폴백: 현재 인터프리터 (uv pip install -- ...)
    """
    if not which("uv"):
        return []
    if pyver:
        return ["uv", "pip", "-p", pyver, "install", "--", *pip_args]
    return ["uv", "pip", "install", "--", *pip_args]


def _net_diag_once(py_for_diag: Optional[str] = None) -> None:
    """최초 1회만 환경 요약 로깅."""
    if _NET_DIAG_ONCE["done"]:
        return
    _NET_DIAG_ONCE["done"] = True
    try:
        ok, rc, so, se = _run_ex(["pip", "--version"])
        if ok:
            logging.info("host pip: %s", so.strip())
        if which("uv"):
            ok, rc, so, se = _run_ex(["uv", "--version"])
            if ok:
                logging.info("uv: %s", so.strip())
        logging.info("DNS pypi.org=%s, HA=%s", _dns_ok("pypi.org"), _dns_ok("pip.home-assistant.io"))
        px = _winhttp_proxy_env_if_needed()
        if px:
            logging.info("WinHTTP proxy detected -> will export: %s", px)
        if py_for_diag:
            _ = _run_ex([py_for_diag, "-c", "import sys;print(sys.version)"])
    except Exception as e:
        logging.warning("net diag 예외: %s", e)


def _ensure_pip_bootstrap(py: str) -> None:
    """대상 파이썬에 pip/wheel/setuptools가 없거나 낡았을 때 업그레이드."""
    _run_ex([py, "-m", "ensurepip", "--upgrade"])
    _run_ex([py, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])


# ===== Port / WS probes ==============================================================

def _port_open(host: str, port: int, timeout: float = 0.6) -> bool:
    with suppress(Exception):
        with socket.create_connection((host, port), timeout=timeout):
            return True
    return False


async def _ws_ping(ws_url: str, timeout: float = 1.5) -> bool:
    try:
        import websockets  # noqa: F401
    except Exception as e:
        # websockets가 현재 컨트롤러 env에 없어도 포트 열림만으로 판단
        try:
            port = int(ws_url.split(":")[2].split("/")[0])
        except Exception as e:
            port = 5580
        return _port_open("localhost", port)

    try:
        import websockets
        async with websockets.connect(ws_url, open_timeout=timeout, close_timeout=timeout) as ws:
            await ws.close()
            return True
    except Exception as e:
        return False


# ===== uv / venv helpers =============================================================
MATTER_VENV_DIR = os.getenv("MATTER_VENV_DIR", ".venv_matter")


def _env_python_from_venv_path(venv_path: str) -> Optional[str]:
    v = os.path.abspath(venv_path)
    cand = os.path.join(v, "Scripts", "python.exe")
    if os.path.exists(cand):
        return cand
    cand = os.path.join(v, "bin", "python")
    if os.path.exists(cand):
        return cand
    return None


def _ensure_python312_venv() -> Optional[str]:
    """Return path to Python 3.12 interpreter for running python-matter-server.
    If current Python is 3.12, reuse it. Otherwise ensure .venv_matter via uv/py launcher.
    """
    cur_ver = (sys.version_info.major, sys.version_info.minor)
    if cur_ver == (3, 12):
        return sys.executable

    # 이미 만들어 둔 venv가 있으면 사용
    py = _env_python_from_venv_path(MATTER_VENV_DIR)
    if py:
        return py

    # 새로 생성
    if not shutil.which("uv"):
        logging.warning("uv 명령을 찾을 수 없습니다. Windows py 런처로 3.12 venv 생성 시도.")
        ok, out = _run(["py", "-3.12", "-m", "venv", MATTER_VENV_DIR])
        if not ok:
            logging.warning("py -3.12 venv 생성 실패: %s", out[-800:])
            return None
        py = _env_python_from_venv_path(MATTER_VENV_DIR)
        if not py:
            logging.warning("생성된 venv에서 python을 찾지 못했습니다: %s", MATTER_VENV_DIR)
            return None
        return py

    # uv 로 venv 생성 (Python 3.12 자동 다운로드/설치 지원)
    ok, out = _run(["uv", "venv", "--python", "3.12", MATTER_VENV_DIR])
    if not ok:
        logging.warning("uv venv --python 3.12 생성 실패: %s", out[-800:])
        return None
    py = _env_python_from_venv_path(MATTER_VENV_DIR)
    if not py:
        logging.warning("uv로 만든 venv에서 python을 찾지 못했습니다: %s", MATTER_VENV_DIR)
        return None
    return py


# ===== BLE prereqs: bleak in *current* controller env ================================

def _ensure_bleak_installed(*, venv_hint: Optional[str] = None, auto_install: bool = True) -> Tuple[bool, str]:
    try:
        import bleak  # noqa: F401
        return True, "bleak OK (current env)"
    except Exception as e:
        miss_msg = f"bleak missing: {e}"
    if not auto_install:
        logging.warning("bleak 미설치(자동설치 비활성): %s", miss_msg)
        return False, miss_msg

    target_py: Optional[str] = None
    if venv_hint:
        target_py = _env_python_from_venv_path(venv_hint)
        if not target_py:
            logging.warning("지정 venv 경로에 python 없음: %s", venv_hint)

    # 현재 env에 설치 시도
    ok, out = _run([sys.executable, "-m", "pip", "install", "--upgrade", "bleak"])
    if not ok:
        logging.warning("현재 env bleak 설치 실패(pip): %s", out[-600:])
        # 힌트 venv가 있고, uv가 있다면 그쪽에도 시도(컨트롤러가 해당 venv로 실행될 때 유효)
        if target_py and shutil.which("uv"):
            ok2, out2 = _run(["uv", "pip", "install", "--python", target_py, "bleak"])
            if not ok2:
                logging.warning("힌트 venv에 bleak 설치 실패: %s", out2[-600:])
                return False, "bleak install failed"
    # 재검증
    try:
        import bleak  # noqa: F401
        return True, "bleak installed"
    except Exception as e:
        logging.warning("bleak import 재시도 실패: %s", e)
        return False, f"bleak import failed: {e}"


def ensure_ble_capable(*, venv_hint: Optional[str] = None, auto_install: bool = True) -> Tuple[bool, str]:
    ok, msg = _ensure_bleak_installed(venv_hint=venv_hint, auto_install=auto_install)
    if not ok:
        return False, msg
    try:
        from bleak import BleakScanner  # type: ignore
        _ = BleakScanner()  # Windows: 초기화에서 BLE 스택 점검
        return True, "BLE stack OK"
    except Exception as e:
        logging.warning("BLE 어댑터 초기화 실패: %s", e)
        return False, f"BLE adapter init failed: {e}"


# ===== Package install helpers =======================================================

def _ensure_pkgs_installed_for_python(
        py: str,
        pkgs: List[str],
        *,
        prefer_binary: bool = True,
        use_ha_index: bool = False,
        timeout: Optional[int] = None,
        wheels_dir: Optional[str] = None,
) -> Tuple[bool, str]:
    """
    패키지 설치 순서:
      1) 오프라인 휠 (--no-index --find-links)
      2) HA 인덱스 (DNS 성공 시) → uv 우선, 실패 시 pip
      3) 일반 PyPI (최후 수단; CHIP은 보통 없음)
    uv rc=2 방지를 위해 -p <버전> + '--' 사용.
    """
    _ensure_pip_bootstrap(py)
    _net_diag_once(py)
    env_proxy = _winhttp_proxy_env_if_needed()

    okv, rcv, sov, sev = _run_ex([py, "-c", "import sys;print(f'{sys.version_info[0]}.{sys.version_info[1]}')"])
    pyver = sov.strip() if okv else None

    base_flags: List[str] = ["--prefer-binary"] if prefer_binary else []

    # 0) 오프라인 전용 강제 여부
    offline_only = _should_offline_only()

    # n. 오프라인 휠
    wheels_dir = wheels_dir or _auto_wheels_hint_dir(pkgs)
    _log_offline_wheels_state(wheels_dir)
    if wheels_dir and os.path.isdir(wheels_dir):
        pip_args = ["--no-index", "--find-links", wheels_dir, *pkgs]
        # uv 먼저
        uv_cmd = _uv_cmd(pyver, pip_args)
        if uv_cmd:
            ok, rc, so, se = _run_ex(uv_cmd, timeout=timeout, env_extra=env_proxy)
            if ok:
                return True, (so or se)
            logging.warning("오프라인(uv) 설치 실패(rc=%s) tail=\n%s", rc, "\n".join(((se or so) or "").splitlines()[-15:]))
        # pip 폴백
        cmd = [py, "-m", "pip", "install", *pip_args]
        ok, rc, so, se = _run_ex(cmd, timeout=timeout, env_extra=env_proxy)
        if ok:
            return True, (so or se)
        logging.warning("오프라인(pip) 설치 실패(rc=%s) tail=\n%s", rc, "\n".join(((se or so) or "").splitlines()[-25:]))

    if offline_only:
        return False, "offline-only 모드: 오프라인 휠 미발견"

    # 2) HA 인덱스 (DNS ok일 때만)
    if use_ha_index and _dns_ok("pip.home-assistant.io"):
        pip_args = [*base_flags, "--extra-index-url", _HA_SIMPLE, *pkgs]
        uv_cmd = _uv_cmd(pyver, pip_args)
        if uv_cmd:
            ok, rc, so, se = _run_ex(uv_cmd, timeout=timeout, env_extra=env_proxy)
            if ok:
                return True, (so or se)
            logging.warning("uv(HA index) 실패(rc=%s) tail=%s", rc, (se or so).splitlines()[-1:])
        cmd = [py, "-m", "pip", "install", "--upgrade", *pip_args]
        ok, rc, so, se = _run_ex(cmd, timeout=timeout, env_extra=env_proxy)
        if ok:
            return True, (so or se)
        logging.warning("pip(HA index) 실패(rc=%s) tail=\n%s", rc, "\n".join(((se or so) or "").splitlines()[-25:]))

    # 3) 일반 PyPI (참고: CHIP 패키지는 보통 없음)
    pip_args = [*base_flags, *pkgs]
    uv_cmd = _uv_cmd(pyver, pip_args)
    if uv_cmd:
        ok, rc, so, se = _run_ex(uv_cmd, timeout=timeout, env_extra=env_proxy)
        if ok:
            return True, (so or se)
        logging.warning("uv(PyPI) 설치 실패(rc=%s) tail=%s", rc, (se or so).splitlines()[-1:])
    cmd = [py, "-m", "pip", "install", "--upgrade", *pip_args]
    ok, rc, so, se = _run_ex(cmd, timeout=timeout, env_extra=env_proxy)
    if ok:
        return True, (so or se)

    return False, (se or so)


def _ensure_chip_layer_for(py: str) -> bool:
    """
    CHIP 레이어(chip.exceptions) 보장:
      - import 프로브
      - 오프라인 휠 → HA 인덱스 → PyPI(정보성; 보통 미존재)
    """
    ok, rc, so, se = _run_ex([py, "-c", "import chip.exceptions; print('OK')"])
    if ok and "OK" in (so or ""):
        return True

    pkgs = ["home-assistant-chip-core", "home-assistant-chip-clusters"]
    logging.info("CHIP 계층 설치 준비(py=%s): %s", py, ", ".join(pkgs))

    ok2, out2 = _ensure_pkgs_installed_for_python(
        py,
        pkgs,
        prefer_binary=True,
        use_ha_index=True,
        timeout=900,
        wheels_dir=_auto_wheels_hint_dir(pkgs),
    )
    if not ok2:
        logging.warning("CHIP 계층 설치 실패: %s", (out2 or "").strip())

    ok3, rc3, so3, se3 = _run_ex([py, "-c", "import chip.exceptions; print('OK')"])
    if ok3 and "OK" in (so3 or ""):
        return True

    last = ((se3 or so3) or "").splitlines()[-1:] or [""]
    logging.warning("CHIP 계층 준비 실패(py=%s). rc=%s last=%s", py, rc3, last)
    return False


def _ensure_server_installed_for(py: str) -> bool:
    """
    대상 인터프리터(py)에 python-matter-server + websockets 설치/검증.
    - uv는 -p <버전> + '--' 구분자 사용
    """

    def _probe() -> bool:
        ok, rc, so, se = _run_ex([
            py,
            "-c",
            "import importlib.util; print('OK' if importlib.util.find_spec('matter_server.server') else 'MISS')",
        ])
        return ok and ("OK" in (so or ""))

    if _probe():
        return True

    _ensure_pip_bootstrap(py)
    okv, rcv, sov, sev = _run_ex([py, "-c", "import sys;print(f'{sys.version_info[0]}.{sys.version_info[1]}')"])
    pyver = sov.strip() if okv else None

    pkgs = ["python-matter-server", "websockets"]
    uv_cmd = _uv_cmd(pyver, pkgs)
    if uv_cmd:
        ok, rc, so, se = _run_ex(uv_cmd, timeout=600)
        if not ok:
            logging.warning("python-matter-server uv 설치 실패(rc=%s) tail=%s", rc, (se or so).splitlines()[-5:])
    else:
        ok, rc, so, se = _run_ex([py, "-m", "pip", "install", "--upgrade", *pkgs], timeout=600)
        if not ok:
            logging.warning("python-matter-server pip 설치 실패(rc=%s) tail=%s", rc, (se or so).splitlines()[-5:])

    if _probe():
        return True

    ok2, rc2, so2, se2 = _run_ex([
        py,
        "-c",
        "import sys, pkgutil; print([m.name for m in pkgutil.iter_modules() if m.name.startswith('matter_server')])",
    ])
    logging.warning(
        "python-matter-server 재확인 실패(py=%s). pkgutil=%s stderr_tail=%s",
        py,
        (so2 or "").strip(),
        (se2 or "").strip().splitlines()[-1:],
    )
    return False


# ===== Native python-matter-server management ========================================

def ensure_native_matter_server(port: int = 5580, *, wait_seconds: float = 14.0) -> bool:
    ws_url = f"ws://localhost:{port}/ws"

    # 3.12 venv 확보
    py = _ensure_python312_venv()
    if not py:
        logging.warning("Python 3.12 인터프리터 준비 실패(.venv_matter 생성/탐색 실패).")
        return False

    # 서버/CHIP 설치 보장
    if not _ensure_server_installed_for(py):
        logging.warning("python-matter-server 설치 실패(py=%s).", py)
        return False
    if not _ensure_chip_layer_for(py):
        logging.warning("CHIP 계층 준비 실패(py=%s).", py)
        return False

    # 이미 떠 있으면 OK (+ WS 핑)
    if _port_open("localhost", port):
        try:
            loop = asyncio.new_event_loop()
            ok_ws = loop.run_until_complete(_ws_ping(ws_url, 1.2))
            loop.close()
        except Exception as e:
            ok_ws = True
        if ok_ws:
            logging.info("Matter 서버가 이미 실행 중입니다: %s", ws_url)
            return True

    # 기동
    candidates = [
        [py, "-m", "matter_server.server", "--port", str(port), "--log-level", "debug"],
        [py, "-m", "matter_server", "--port", str(port)],
        ["matter-server", "--port", str(port)],
    ]

    proc: Optional[subprocess.Popen] = None
    last_err: str = ""
    for cmd in candidates:
        try:
            logging.info("python-matter-server 시작 시도: %s", " ".join(cmd))
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            time.sleep(0.6)
            if _port_open("localhost", port):
                break
            if proc.poll() is not None:
                so, se = proc.communicate(timeout=0.3)
                if se:
                    last_err = se.strip().splitlines()[-1] if se.strip() else ""
                    logging.warning("즉시 종료(stderr last): %s", last_err)
                proc = None
        except Exception as e:
            logging.warning("server start 예외: %s", e)
            proc = None

    if not proc:
        logging.warning("python-matter-server 실행 실패: 후보 명령들이 모두 실패 (py=%s).", py)
        return False

    # WS 준비 대기
    deadline = time.time() + wait_seconds
    ok = False
    while time.time() < deadline:
        if _port_open("localhost", port):
            try:
                loop = asyncio.new_event_loop()
                ok = loop.run_until_complete(_ws_ping(ws_url, 1.2))
                loop.close()
            except Exception as e:
                ok = True
        if ok:
            break
        if proc.poll() is not None:
            try:
                so, se = proc.communicate(timeout=0.4)
            except Exception as e:
                so, se = "", ""
            if se:
                last = se.strip().splitlines()[-1] if se.strip() else ""
                logging.warning("matter-server 조기 종료(stderr last): %s", last)
            if so:
                logging.info("matter-server stdout(last 1k): %s", so[-1000:])
            break
        time.sleep(0.6)

    if not ok:
        logging.warning("python-matter-server WS 준비 확인 실패: %s", ws_url)
        logging.warning("Windows 방화벽 허용 여부, 관리자 권한, 그리고 %s 로 실행 중인지 점검하세요.", py)
        return False

    logging.info("python-matter-server 기동 완료: %s (py=%s)", ws_url, py)
    return True


# ===== Env defaults & SSID hint ======================================================

def _ensure_native_backend_env() -> None:
    os.environ.setdefault("MATTER_BACKEND", "native")  # Docker 폴백 금지
    os.environ.setdefault("MATTER_SERVER_PORT", "5580")


def _warn_if_5ghz_ssid(ssid: Optional[str]) -> None:
    if not ssid:
        return
    s = ssid.lower()
    if re.search(r"(?<![a-z0-9])5g(hz)?(?![a-z0-9])", s):
        logging.warning("SSID가 5GHz로 보입니다(%s). 다수의 Wi-Fi 기반 Matter 플러그는 2.4GHz만 지원합니다.", ssid)


# ===== Lazy project imports ==========================================================

def _get_matter_controller() -> Tuple[Optional[Any], Optional[Any]]:
    try:
        from pk_internal_tools.pk_objects.pk_matter_controller import (  # type: ignore
            PkMatterController,
            MatterCommissionConfig,
        )
        return PkMatterController, MatterCommissionConfig
    except Exception as e:
        logging.warning("PkMatterController import 실패: %s", e)
        return None, None


def _get_env_var_return():
    try:
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed  # type: ignore
        return ensure_env_var_completed
    except Exception as e:
        return None


def _get_wifi_creds() -> Tuple[Optional[str], Optional[str]]:
    try:
        from pk_internal_tools.pk_functions.ensure_wifi_pw_printed_fixed import ensure_wifi_pw_printed_fixed  # type: ignore
    except Exception as e:
        return None, None
    try:
        return ensure_wifi_pw_printed_fixed()
    except Exception as e:
        logging.warning("Wi-Fi 자격증명 자동조회 실패: %s", e)
        return None, None


# ===== Discover helper ===============================================================
async def _discover_with_retry(controller, tries: int = 3, delay: float = 0.8) -> List[Any]:
    devices: List[Any] = []
    for i in range(tries):
        try:
            devices = await controller.discover_devices()
        except Exception as e:
            logging.warning("discover_devices 시도%d 실패: %s", i + 1, e)
            devices = []
        if not devices:
            cached = controller.get_devices() or []
            if cached:
                return cached
        if devices:
            return devices
        await asyncio.sleep(delay * (2 ** i))
    return controller.get_devices() or []


# ===== Public API: control & list ====================================================
async def ensure_matter_device_controlled(
        device_identifier: str,
        action: str = "toggle",
        commission_code: Optional[str] = None,
        wifi_ssid: Optional[str] = None,
        wifi_password: Optional[str] = None,
) -> bool:
    """Control a Matter device via PkMatterController.
    If commission_code is given, performs commissioning first (BLE/SoftAP expected).
    """
    _ensure_native_backend_env()

    # 서버 준비(항상 3.12 실행 보장)
    port = int(os.getenv("MATTER_SERVER_PORT", "5580"))
    if not ensure_native_matter_server(port=port):
        return False

    PkMatterController, MatterCommissionConfig = _get_matter_controller()
    if not PkMatterController:
        return False

    try:
        async with PkMatterController() as controller:
            # Commission if requested
            if commission_code:
                ok_ble, reason = ensure_ble_capable(
                    venv_hint=os.getenv("UV_VENV_PATH", ".venv"),
                    auto_install=True,
                )
                if not ok_ble:
                    logging.warning("BLE 준비 실패(계속 진행 가능성 있음): %s", reason)
                if wifi_ssid is None or wifi_password is None:
                    ssid, pw = _get_wifi_creds()
                    wifi_ssid = wifi_ssid or ssid
                    wifi_password = wifi_password or pw
                _warn_if_5ghz_ssid(wifi_ssid)

                logging.info("새 장치 커미션 시작: %s", ensure_sensitive_info_masked(commission_code))
                cfg = MatterCommissionConfig(
                    commission_code=commission_code,
                    wifi_ssid=wifi_ssid,
                    wifi_password=wifi_password,
                )
                ok = await controller.commission_device(cfg)
                if not ok:
                    logging.warning("장치 커미션 실패(Matter 서버/BLE 가용성/코드/네트워크를 점검).")
                    return False
                logging.info("장치 커미션 성공")

            # Locate device
            device = None
            node_id = _parse_node_id_maybe(device_identifier)
            if node_id is not None:
                device = controller.get_device(node_id)
                if not device:
                    logging.info("node_id %s 장치 캐시 미스 → discover", node_id)
                    await _discover_with_retry(controller)
                    device = controller.get_device(node_id)
            else:
                device = controller.find_device_by_name(device_identifier)
                if not device:
                    await _discover_with_retry(controller)
                    device = controller.find_device_by_name(device_identifier)

            if not device:
                logging.warning("장치를 찾을 수 없습니다: %s", device_identifier)
                devices = controller.get_devices()
                if devices:
                    logging.info("사용 가능한 장치 목록:")
                    for d in devices:
                        logging.info(
                            "  - ID: %s, 이름: %s",
                            getattr(d, "node_id", "?"),
                            getattr(d, "display_name", "?"),
                        )
                else:
                    logging.info("연결된 Matter 장치가 없습니다.")
                return False

            # Act
            name = getattr(device, "display_name", str(device_identifier))
            act = (action or "").lower()
            logging.info("장치 제어: %s -> %s", name, act)
            if act == "on":
                result = await controller.turn_on(device.node_id)
            elif act == "off":
                result = await controller.turn_off(device.node_id)
            elif act == "toggle":
                result = await controller.toggle(device.node_id)
            elif act == "status":
                state = await controller.get_onoff_state(device.node_id)
                if state is None:
                    logging.warning("%s 상태 확인 실패", name)
                    return False
                logging.info("%s 현재 상태: %s", name, "ON" if state else "OFF")
                return True
            else:
                logging.warning("지원하지 않는 액션: %s", action)
                return False

            if result:
                logging.info("%s %s 성공", name, act)
                if act in ("on", "off", "toggle"):
                    await asyncio.sleep(1)
                    new_state = await controller.get_onoff_state(device.node_id)
                    if new_state is not None:
                        logging.info("변경된 상태: %s", "ON" if new_state else "OFF")
                return True
            else:
                logging.warning("%s %s 실패", name, act)
                return False

    except Exception as e:
        logging.warning("Matter 장치 제어 중 예외: %s", e)
        return False


async def list_matter_devices() -> List[Dict[str, Any]]:
    _ensure_native_backend_env()
    port = int(os.getenv("MATTER_SERVER_PORT", "5580"))
    if not ensure_native_matter_server(port=port):
        return []

    PkMatterController, _ = _get_matter_controller()
    if not PkMatterController:
        return []

    try:
        async with PkMatterController() as controller:
            devices = await _discover_with_retry(controller)
            result: List[Dict[str, Any]] = []
            for device in devices:
                try:
                    state = await controller.get_onoff_state(device.node_id)
                except Exception as e:
                    logging.warning("상태 조회 실패(node_id=%s): %s", getattr(device, "node_id", "?"), e)
                    state = None
                dtype = getattr(device, "device_type", None)
                dtype_val = getattr(dtype, "value", None) if dtype is not None else None
                info = {
                    "node_id": getattr(device, "node_id", None),
                    "name": getattr(device, "display_name", None),
                    "vendor": getattr(device, "vendor_name", None),
                    "product": getattr(device, "product_name", None),
                    "type": dtype_val or (str(dtype) if dtype is not None else None),
                    "is_online": getattr(device, "is_online", None),
                    "current_state": "ON" if state else "OFF" if state is not None else "UNKNOWN",
                }
                result.append(info)
                logging.info("장치: %s", info)
            return result
    except Exception as e:
        logging.warning("Matter 장치 목록 조회 중 예외: %s", e)
        return []


# ===== Sync wrappers =================================================================

def ensure_matter_device_controlled_sync(
        device_identifier: str,
        action: str = "toggle",
        commission_code: Optional[str] = None,
        wifi_ssid: Optional[str] = None,
        wifi_password: Optional[str] = None,
) -> bool:
    return asyncio.run(
        ensure_matter_device_controlled(
            device_identifier=device_identifier,
            action=action,
            commission_code=commission_code,
            wifi_ssid=wifi_ssid,
            wifi_password=wifi_password,
        )
    )


def list_matter_devices_sync() -> List[Dict[str, Any]]:
    return asyncio.run(list_matter_devices())


# ===== Convenience for P110M & demo flow =============================================
async def ensure_matter_smart_plug_on(
        commission_code: Optional[str] = None,
        wifi_ssid: Optional[str] = None,
        wifi_password: Optional[str] = None,
) -> bool:
    if commission_code is None:
        ensure_env_var_completed = _get_env_var_return()
        if ensure_env_var_completed:
            commission_code = ensure_env_var_completed_2025_11_23(
                "P110M_MATTER_COMMISSION_CODE",
                "Please enter the Matter Commission Code: ",
                mask_log=True,
            )
        else:
            commission_code = input("Matter Commission Code: ").strip()
        if not commission_code:
            logging.warning("Commission Code 누락으로 진행 불가.")
            return False
    return await ensure_matter_device_controlled("1", "on", commission_code, wifi_ssid, wifi_password)


async def ensure_pk_p110m_off(
        commission_code: Optional[str] = None,
        wifi_ssid: Optional[str] = None,
        wifi_password: Optional[str] = None,
) -> bool:
    if commission_code is None:
        ensure_env_var_completed = _get_env_var_return()
        if ensure_env_var_completed:
            commission_code = ensure_env_var_completed_2025_11_23(
                "P110M_MATTER_COMMISSION_CODE",
                "Please enter the Matter Commission Code: ",
                mask_log=True,
            )
        else:
            commission_code = input("Matter Commission Code: ").strip()
        if not commission_code:
            logging.warning("Commission Code 누락으로 진행 불가.")
            return False
    return await ensure_matter_device_controlled("1", "off", commission_code, wifi_ssid, wifi_password)


async def ensure_pk_p110m_toggle(
        commission_code: Optional[str] = None,
        wifi_ssid: Optional[str] = None,
        wifi_password: Optional[str] = None,
) -> bool:
    if commission_code is None:
        ensure_env_var_completed = _get_env_var_return()
        if ensure_env_var_completed:
            commission_code = ensure_env_var_completed_2025_11_23(
                "P110M_MATTER_COMMISSION_CODE",
                "Please enter the Matter Commission Code: ",
                mask_log=True,
            )
        else:
            commission_code = input("Matter Commission Code: ").strip()
        if not commission_code:
            logging.warning("Commission Code 누락으로 진행 불가.")
            return False
    return await ensure_matter_device_controlled("1", "toggle", commission_code, wifi_ssid, wifi_password)


@ensure_seconds_measured
async def ensure_matter_smart_controllable():
    """Demo flow: list → commission (if none) → basic control test."""
    logging.debug("=== Matter 장치 제어 가능성 테스트 시작")

    # Load commission code via project helper or prompt
    env_return = _get_env_var_return()
    if env_return:
        matter_commission_code = env_return(
            "P110M_MATTER_COMMISSION_CODE",
            "Please enter the Matter Commission Code: ",
            mask_log=True,
        )
    else:
        matter_commission_code = input("Matter Commission Code: ").strip()

    # Wi-Fi creds 자동 획득(가능 시)
    wifi_ssid, wifi_password = _get_wifi_creds()
    _warn_if_5ghz_ssid(wifi_ssid)

    # n. List devices
    logging.debug("1. 연결된 Matter 장치 목록 확인…")
    devices = await list_matter_devices()

    # 2) Commission if none
    if not devices:
        logging.debug("연결된 장치 없음 → 커미셔닝 시도: %s", ensure_sensitive_info_masked(matter_commission_code))
        await ensure_matter_device_controlled(
            device_identifier="1",
            action="status",
            commission_code=matter_commission_code,
            wifi_ssid=wifi_ssid,
            wifi_password=wifi_password,
        )
        logging.debug("2.1. 커미셔닝 후 장치 목록 재확인…")
        devices = await list_matter_devices()
        if not devices:
            logging.debug("커미셔닝 실패 또는 장치 미발견. Wi-Fi/코드 상태 확인 필요.")
            logging.debug("=== 테스트 종료")
            return

    # 3) Control quick test on first device
    logging.debug("3. 장치 제어 테스트 시작:")
    for d in devices:
        logging.debug("ID: %s, 이름: %s, 현재 상태: %s", d['node_id'], d['name'], d['current_state'])

    target = devices[0]
    device_id = str(target['node_id'])
    name = target['name']

    logging.debug("3.1. 대상 '%s'(ID: %s) 제어 테스트", name, device_id)
    await ensure_matter_device_controlled(device_id, "status")
    await asyncio.sleep(1)
    await ensure_matter_device_controlled(device_id, "on")
    await asyncio.sleep(1.5)
    await ensure_matter_device_controlled(device_id, "off")
    await asyncio.sleep(1.5)
    await ensure_matter_device_controlled(device_id, "toggle")
    await asyncio.sleep(1)

    logging.debug("'%s' 제어 테스트 완료.", name)
    logging.debug("=== 모든 테스트 완료")


if __name__ == "__main__":
    asyncio.run(ensure_matter_smart_controllable())
