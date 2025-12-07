"""Run finance service build/test shell script under Linux/WSL.
If executed on Windows, guide the user to use WSL/Linux.
"""
from pathlib import Path
import platform
import subprocess
import sys


def main(stream: bool = True, tmux: bool = True) -> None:
    """Run shell script; if *stream* is True, show real-time output."""
    if platform.system() == "Windows":
        print("❌ 이 스크립트는 WSL/Linux 환경에서만 실행 가능합니다. WSL 터미널에서 실행해 주세요.")
        sys.exit(1)

    project_root = Path(__file__).resolve().parents[1]
    deploy_dir = project_root / "pkg_finance_invest_assist" / "deployment"
    sh_file = deploy_dir / "smart_person_ai_build_test.sh"

    if not sh_file.exists():
        print(f"❌ Shell script not found: {sh_file}")
        sys.exit(1)

    # 실행 권한 보장
    sh_file.chmod(sh_file.stat().st_mode | 0o111)

    # ---------------------------- tmux mode -----------------------------
    import shutil, os, select, pty
    if tmux and shutil.which("tmux"):
        tmux_session = "smart_person_ai_build"
        sh_run = f"bash {sh_file}; exec bash"  # build 후 bash 유지

        if "TMUX" in os.environ:
            # 이미 tmux 안 → 새 window 생성
            subprocess.run(["tmux", "new-window", "-n", tmux_session], check=True)
            subprocess.run(["tmux", "send-keys", "-t", tmux_session, sh_run, "C-m"], check=True)
            subprocess.run(["tmux", "split-window", "-v", "-t", tmux_session], check=True)
            subprocess.run(["tmux", "select-window", "-t", tmux_session], check=True)
            sys.exit(0)
        else:
            # tmux 외부 → detached 세션 만들고 attach
            subprocess.run(["tmux", "new-session", "-d", "-s", tmux_session], check=True)
            subprocess.run(["tmux", "send-keys", "-t", f"{tmux_session}.0", sh_run, "C-m"], check=True)
            subprocess.run(["tmux", "split-window", "-v", "-t", tmux_session], check=True)
            subprocess.run(["tmux", "attach", "-t", tmux_session])
            sys.exit(0)

    # ---------------------- streaming (pty) fallback --------------------
    if stream:
        # Use pseudo-TTY so docker compose streams nicely
        import pty, os, select

        master_fd, slave_fd = pty.openpty()
        proc = subprocess.Popen(
            ["bash", str(sh_file)],
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            text=False,
            bufsize=0,
        )
        os.close(slave_fd)
        try:
            while True:
                r, _, _ = select.select([master_fd], [], [], 0.1)
                if master_fd in r:
                    output = os.read(master_fd, 1024)
                    if not output:
                        break
                    sys.stdout.buffer.write(output)
                    sys.stdout.flush()
                if proc.poll() is not None:
                    # process ended; drain remaining
                    remaining = os.read(master_fd, 1024)
                    if remaining:
                        sys.stdout.buffer.write(remaining)
                        sys.stdout.flush()
                    break
        except KeyboardInterrupt:
            print("⏹️  사용자 중단 – 컨테이너 정리 시도")
            proc.terminate()
        finally:
            os.close(master_fd)
        sys.exit(proc.returncode)
    else:
        # simple blocking run (no stream)
        try:
            subprocess.run(["bash", str(sh_file)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"💥 빌드 스크립트 실패: {e}")
            sys.exit(e.returncode)


if __name__ == "__main__":
    main()
