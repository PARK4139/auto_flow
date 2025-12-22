def ensure_repo_cloned_via_git(repo_url: str, d_dst: str):
    """
    Clone a Git repository with defensive checks:
    - Force HTTPS for GitHub URLs
    - If destination exists as the same repo, do 'git pull' instead of cloning
    - If destination exists with a different repo, backup then clone
    - Create destination parent directory if missing
    - Ensure a valid working branch is checked out (prefer 'main', then 'master')
    """
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    import subprocess
    import os
    import shutil
    import time
    import uuid

    def normalize_url(url: str) -> str:
        if url.startswith("http://github.com/"):
            return "https://" + url[len("http://"):]
        return url

    def is_git_repo(path: str) -> bool:
        return os.path.isdir(os.path.join(path, ".git"))

    def run(cmd, cwd=None, check=True, text=True):
        # capture_output=True so we can inspect stdout/stderr if needed
        return subprocess.run(cmd, cwd=cwd, check=check, text=text, capture_output=True)

    def get_remote_url(path: str) -> str | None:
        try:
            out = run(["git", "-C", path, "remote", "get-url", "origin"])
            return out.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def detect_remote_branch(path: str) -> str | None:
        """
        Returns: 'main' if origin/main exists; else 'master' if exists; else first head; else None.
        """
        try:
            out = run(["git", "-C", path, "ls-remote", "--heads", "origin"])
            heads = []
            for ln in out.stdout.splitlines():
                if "\trefs/heads/" in ln:
                    heads.append(ln.split("\t")[1].split("refs/heads/")[1])
            if "main" in heads:
                return "main"
            if "master" in heads:
                return "master"
            return heads[0] if heads else None
        except subprocess.CalledProcessError:
            return None

    def ensure_checked_out_branch(path: str):
        """
        Ensure working copy is on a valid named branch tracking origin.
        Handles detached HEAD / remote HEAD mismatch cases.
        """
        try:
            cur = run(["git", "-C", path, "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
        except subprocess.CalledProcessError:
            cur = "HEAD"

        if cur not in ("HEAD", "HEAD (no branch)"):
            return  # already on a branch

        b = detect_remote_branch(path)
        if not b:
            # Remote has no heads (empty repo). Nothing to checkout.
            return
        # Create/switch local branch to track origin/b
        run(["git", "-C", path, "checkout", "-B", b, f"origin/{b}"])

    # n. URL normalize
    repo_url = normalize_url(repo_url)

    # 2) Ensure parent dir
    parent = os.path.abspath(os.path.join(d_dst, os.pardir))
    os.makedirs(parent, exist_ok=True)

    # 3) Destination logic
    if os.path.exists(d_dst):
        if is_git_repo(d_dst):
            current_remote = get_remote_url(d_dst)
            if current_remote and normalize_url(current_remote) == repo_url:
                # same repo → update
                run(["git", "-C", d_dst, "fetch", "--all", "--prune"])
                # make sure we are on a valid branch before pull
                ensure_checked_out_branch(d_dst)
                try:
                    run(["git", "-C", d_dst, "pull", "--ff-only"])
                except subprocess.CalledProcessError:
                    # If pull fails due to upstream/branch state, try once more after enforcing checkout
                    ensure_checked_out_branch(d_dst)
                    run(["git", "-C", d_dst, "pull", "--ff-only"])
                logging.debug(f'''git pulled {repo_url} at {d_dst} ''')
                return
            else:
                # different repo → backup then clone fresh
                backup_name = f"{d_dst}_backup_{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
                shutil.move(d_dst, backup_name)
                logging.debug(f"Backup existing repo to: {backup_name}")
        else:
            # exists but not a git repo → backup then clone
            backup_name = f"{d_dst}_backup_{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
            shutil.move(d_dst, backup_name)
            logging.debug(f"Backup existing folder to: {backup_name}")

    # 4) Fresh clone
    run(["git", "clone", repo_url, d_dst])
    # Some remotes (esp. freshly created bare repos) have HEAD pointing to a non-existent ref.
    # Ensure we checkout a valid branch (main > master).
    ensure_checked_out_branch(d_dst)
    logging.debug(f'''git cloned {repo_url} at {d_dst} ''')


if __name__ == "__main__":

    import os
    import shutil
    import tempfile
    import subprocess
    import time
    import stat
    from pathlib import Path

    def _rm_readonly_retry(func, path, exc_info):
        # Clear read-only bit then retry, with a tiny wait (Windows .git objects)
        try:
            os.chmod(path, stat.S_IWRITE)
        except Exception as e:
            pass
        try:
            func(path)
        except PermissionError:
            time.sleep(0.2)
            func(path)

    temp_base = Path(tempfile.gettempdir()) / "test_git_clone"
    if temp_base.exists():
        shutil.rmtree(temp_base, onerror=_rm_readonly_retry)
    temp_base.mkdir(parents=True)

    bare_repo_main = temp_base / "dummy_main_repo.git"
    bare_repo_other = temp_base / "dummy_other_repo.git"
    subprocess.run(["git", "init", "--bare", str(bare_repo_main)], check=True)
    subprocess.run(["git", "init", "--bare", str(bare_repo_other)], check=True)

    # --- main repo 준비 ---
    temp_work = temp_base / "temp_work"
    subprocess.run(["git", "clone", str(bare_repo_main), str(temp_work)], check=True)
    (temp_work / "README.md").write_text("# Dummy Main Repo\n")
    subprocess.run(["git", "-C", str(temp_work), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(temp_work), "commit", "-m", "Initial commit"], check=True)
    subprocess.run(["git", "-C", str(temp_work), "push", "origin", "HEAD:main"], check=True)
    # bare repo HEAD → main 으로 고정 (remote HEAD mismatch 방지)
    subprocess.run(["git", "--git-dir", str(bare_repo_main), "symbolic-ref", "HEAD", "refs/heads/main"], check=True)
    time.sleep(0.1)
    shutil.rmtree(temp_work, onerror=_rm_readonly_retry)

    # --- other repo 준비 ---
    temp_work = temp_base / "temp_work"
    subprocess.run(["git", "clone", str(bare_repo_other), str(temp_work)], check=True)
    (temp_work / "README.md").write_text("# Dummy Other Repo\n")
    subprocess.run(["git", "-C", str(temp_work), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(temp_work), "commit", "-m", "Initial commit"], check=True)
    subprocess.run(["git", "-C", str(temp_work), "push", "origin", "HEAD:main"], check=True)
    subprocess.run(["git", "--git-dir", str(bare_repo_other), "symbolic-ref", "HEAD", "refs/heads/main"], check=True)
    time.sleep(0.1)
    shutil.rmtree(temp_work, onerror=_rm_readonly_retry)

    # --- 테스트 로직 ---
    REPO_MAIN = str(bare_repo_main)
    REPO_OTHER = str(bare_repo_other)

    # NOTE: if this file itself is ensure_repo_cloned_via_git.py, the import below is redundant.
    # from pk_internal_tools.pk_functions.ensure_repo_cloned_via_git import ensure_repo_cloned_via_git

    def _get_remote_url(path: Path) -> str:
        try:
            return subprocess.check_output(
                ["git", "-C", str(path), "remote", "get-url", "origin"],
                text=True
            ).strip()
        except subprocess.CalledProcessError:
            return None

    dst = temp_base / "repo"

    print("[TEST 1] 빈 폴더 → 첫 clone")
    ensure_repo_cloned_via_git(REPO_MAIN, str(dst))
    assert (dst / ".git").exists(), "첫 clone 실패"

    print("[TEST 2] 같은 repo → pull 시도")
    ensure_repo_cloned_via_git(REPO_MAIN, str(dst))

    print("[TEST 3] 다른 repo → 백업 후 clone")
    ensure_repo_cloned_via_git(REPO_OTHER, str(dst))
    assert _get_remote_url(dst) == REPO_OTHER, "다른 repo clone 실패"

    print("[TEST 4] Git repo 아님 → 백업 후 clone")
    shutil.rmtree(dst, onerror=_rm_readonly_retry)
    dst.mkdir()
    (dst / "dummy.txt").write_text("not a git repo")
    ensure_repo_cloned_via_git(REPO_MAIN, str(dst))
    assert _get_remote_url(dst) == REPO_MAIN, "Git repo 아님 처리 실패"

    print(" 모든 테스트 통과")
