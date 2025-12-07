from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_executed_advanced(
    diff_source="git",          # "git" | "file" | "text"
    diff_value=None,            # path(str/Path) for "file", the diff string for "text", ignored for "git"
    instruction=(
        "You are a coding assistant that returns only a unified diff (git-style).\n"
        "- Output ONLY a valid patch (no prose, no code fences).\n"
        "- Keep changes surgical; do not reformat unrelated lines.\n"
        "- Use minimal context when safe (e.g., -U0 is OK).\n"
        "- Paths must match working tree exactly so `git apply` succeeds.\n"
        "Given the ORIGINAL diff below, produce an improved/cleaned unified diff that applies cleanly."
    ),
    save_dir=None,              # where to save generated patch; temp if None
    apply_patch=True,           # apply via `git apply --index --reject`
    timeout_sec=600,
    as_json=False,              # normally False (text diff)
    cwd=None,                   # repo root (None = current)
    # --- debugging knobs ---
    debug=True,
    keep_temps=False,
    validate_patch=True,
    dry_run=False
):
    """
    Submit a unified diff to Gemini via STDIN -> get unified diff -> save -> (optionally) validate/apply via git.

    Returns dict:
      {
        "ok": bool, "rc": int,
        "diff_in": str, "patch_out": str,
        "applied": bool, "rej_hints": str,
        "patch_path": str or "",
        "temp_files": [...], "steps": [...], "diagnostics": {...}
      }
    """
    # --- lazy imports
    import os
    import sys
    import shutil
    import subprocess
    import tempfile
    import logging
    import traceback
    from pathlib import Path
    from datetime import datetime
    import platform

    steps, temp_files = [], []
    diag = {"env": {}, "cmds": {}, "lengths": {}, "patch_head": ""}

    def _now(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ---------- subprocess helpers (robust decoding) ----------
    def _run_capture(cmd_args, timeout=None, cwd=None, env=None, step_name=""):
        if debug:
            steps.append({"ts": _now(), "step": f"{step_name or 'run'}:exec", "cmd": cmd_args, "cwd": cwd})
        try:
            proc = subprocess.Popen(
                cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, env=env
            )
            try:
                out_b, err_b = proc.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.kill()
                out_b, err_b = proc.communicate()
            rc = proc.returncode

            def _dec(b: bytes) -> str:
                if b is None: return ""
                for enc in ("utf-8", "cp949", "latin-1"):
                    try:
                        return b.decode(enc, errors="strict" if enc == "utf-8" else "replace")
                    except Exception:
                        continue
                return b.decode("latin-1", errors="replace")

            out = _dec(out_b)
            err = _dec(err_b)

            if debug:
                steps.append({
                    "ts": _now(), "step": f"{step_name or 'run'}:done",
                    "rc": rc, "stdout_len": len(out), "stderr_len": len(err),
                    "stdout_head": out[:300], "stderr_head": err[:300],
                })
            return rc, out, err
        except Exception as e:
            if debug:
                steps.append({"ts": _now(), "step": f"{step_name or 'run'}:exception", "error": str(e)})
            return 255, "", f"_run_capture exception: {e}"

    def _run_capture_with_stdin(cmd_args, input_text, timeout=None, cwd=None, env=None, step_name=""):
        """
        Run process with given input_text piped to STDIN. Return (rc, stdout_str, stderr_str).
        Avoids command-line length limits and matches gemini's non-interactive usage.
        """
        if debug:
            steps.append({"ts": _now(), "step": f"{step_name or 'run_stdin'}:exec", "cmd": cmd_args, "cwd": cwd, "stdin_bytes": len((input_text or '').encode('utf-8'))})
        try:
            proc = subprocess.Popen(
                cmd_args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd,
                env=env
            )
            try:
                out_b, err_b = proc.communicate(input=(input_text or "").encode("utf-8"), timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.kill()
                out_b, err_b = proc.communicate()
            rc = proc.returncode

            def _dec(b: bytes) -> str:
                if b is None: return ""
                for enc in ("utf-8", "cp949", "latin-1"):
                    try:
                        return b.decode(enc, errors="strict" if enc == "utf-8" else "replace")
                    except Exception:
                        continue
                return b.decode("latin-1", errors="replace")

            out = _dec(out_b)
            err = _dec(err_b)
            if debug:
                steps.append({
                    "ts": _now(), "step": f"{step_name or 'run_stdin'}:done",
                    "rc": rc, "stdout_len": len(out), "stderr_len": len(err),
                    "stdout_head": out[:300], "stderr_head": err[:300],
                })
            return rc, out, err
        except Exception as e:
            if debug:
                steps.append({"ts": _now(), "step": f"{step_name or 'run_stdin'}:exception", "error": str(e)})
            return 255, "", f"_run_capture exception: {e}"

    def _write_temp(text: str, suffix=".diff", tag="tmp"):
        f = tempfile.NamedTemporaryFile(prefix="gemini_", suffix=suffix, delete=False)
        p = Path(f.name)
        p.write_text(text or "", encoding="utf-8")
        f.close()
        temp_files.append(str(p))
        if debug:
            steps.append({"ts": _now(), "step": "write_temp", "path": str(p), "bytes": len((text or "").encode("utf-8")), "tag": tag})
        return str(p)

    # ---------- PATH & executable resolution ----------
    def _ensure_prefix_on_path(child_env):
        rc, out, _ = _run_capture(["npm", "config", "get", "prefix"], timeout=10, env=child_env, step_name="probe:npm_prefix")
        prefix = (out or "").strip() if rc == 0 else ""
        paths_to_add = []
        if prefix:
            paths_to_add.append(prefix)
            bin_dir = os.path.join(prefix, "bin")
            if os.path.isdir(bin_dir):
                paths_to_add.append(bin_dir)
        sep = ";" if os.name == "nt" else ":"
        cur = child_env.get("PATH", "")
        for p in paths_to_add:
            if p and p not in cur:
                cur = p + (sep + cur if cur else "")
        child_env["PATH"] = cur
        return prefix

    def _resolve_gemini_cmd(child_env):
        override = os.environ.get("GEMINI_CMD")
        if override:
            if os.name == "nt" and override.lower().endswith(".ps1"):
                return ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", override]
            return [override]
        found = shutil.which("gemini")
        if found:
            return [found]
        if os.name == "nt":
            prefix = _ensure_prefix_on_path(child_env)
            candidates = []
            if prefix:
                candidates += [
                    os.path.join(prefix, "gemini.cmd"),
                    os.path.join(prefix, "gemini.ps1"),
                ]
            for c in candidates:
                if os.path.isfile(c):
                    if c.lower().endswith(".ps1"):
                        return ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", c]
                    return [c]
        return ["gemini"]

    # ---------- child env ----------
    child_env = os.environ.copy()
    child_env.setdefault("LC_ALL", "C.UTF-8")
    child_env.setdefault("LANG", "C.UTF-8")
    _ensure_prefix_on_path(child_env)
    gemini_cmd_list = _resolve_gemini_cmd(child_env)
    diag["cmds"]["gemini_resolved"] = " ".join(gemini_cmd_list)

    # diagnostics (best-effort)
    if debug:
        try:
            for name, cmd in {
                "node_version": ["node", "-v"],
                "npm_version": ["npm", "-v"],
            }.items():
                rc, out, _ = _run_capture(cmd, timeout=10, env=child_env, step_name=f"probe:{name}")
                diag["env"][name] = (out or "").strip()
            rc, out, _ = _run_capture(gemini_cmd_list + ["--version"], timeout=10, env=child_env, step_name="probe:gemini_version")
            diag["env"]["gemini_version"] = (out or "").strip()
            diag["env"]["PATH_head"] = child_env.get("PATH", "")[:200]
            diag["env"]["platform"] = platform.platform()
        except Exception:
            pass

    # n. acquire diff ----------------------------------------------------------
    try:
        if diff_source == "git":
            cmd_diff = ["git", "diff", "-U0"]
            diag["cmds"]["git_diff"] = " ".join(cmd_diff)
            rc, out, err = _run_capture(cmd_diff, timeout=timeout_sec, cwd=cwd, env=child_env, step_name="git:diff")
            out = out or ""
            if rc != 0:
                return {"ok": False, "rc": rc, "diff_in": "", "patch_out": "", "applied": False,
                        "rej_hints": (out or err)[:400], "patch_path": "", "temp_files": temp_files,
                        "steps": steps, "diagnostics": diag}
            if not out.strip():
                return {"ok": True, "rc": 0, "diff_in": "", "patch_out": "", "applied": False,
                        "rej_hints": "No changes.", "patch_path": "", "temp_files": temp_files,
                        "steps": steps, "diagnostics": diag}
            diff_in = out
            _write_temp(diff_in, suffix=".diff", tag="input_diff")

        elif diff_source == "file":
            path = str(Path(diff_value).resolve())
            try:
                diff_in = Path(path).read_text(encoding="utf-8")
            except UnicodeDecodeError:
                try:
                    diff_in = Path(path).read_text(encoding="cp949", errors="replace")
                except Exception:
                    diff_in = Path(path).read_text(encoding="latin-1", errors="replace")
            if not (diff_in or "").strip():
                return {"ok": False, "rc": 2, "diff_in": "", "patch_out": "", "applied": False,
                        "rej_hints": "Empty diff file.", "patch_path": "", "temp_files": temp_files,
                        "steps": steps, "diagnostics": diag}

        elif diff_source == "text":
            diff_in = str(diff_value or "")
            if not diff_in.strip():
                return {"ok": False, "rc": 2, "diff_in": "", "patch_out": "", "applied": False,
                        "rej_hints": "Empty diff text.", "patch_path": "", "temp_files": temp_files,
                        "steps": steps, "diagnostics": diag}

        else:
            return {"ok": False, "rc": 2, "diff_in": "", "patch_out": "", "applied": False,
                    "rej_hints": "Invalid diff_source.", "patch_path": "", "temp_files": temp_files,
                    "steps": steps, "diagnostics": diag}

    except Exception:
        return {"ok": False, "rc": 3, "diff_in": "", "patch_out": "", "applied": False,
                "rej_hints": "prep failed", "patch_path": "", "temp_files": temp_files,
                "steps": steps + [{"ts": _now(), "step": "prep:exception", "error": traceback.format_exc()}],
                "diagnostics": diag}

    # 2) call gemini via STDIN -------------------------------------------------
    try:
        # Build one big prompt text to pipe into STDIN
        prompt_text = (
            f"{instruction}\n\n=== ORIGINAL DIFF START ===\n{diff_in}\n=== ORIGINAL DIFF END ===\n"
        )
        if keep_temps:
            _write_temp(prompt_text, suffix=".txt", tag="stdin_prompt")

        out_fmt = "json" if as_json else "text"
        # simplest non-interactive: just set output and feed stdin
        cmd = gemini_cmd_list + ["--output", out_fmt]
        # (선택) 아주 짧은 제목을 -p 로 넘길 수도 있음:
        # cmd = gemini_cmd_list + ["--output", out_fmt, "-p", "Apply unified diff generation to stdin"]

        diag["cmds"]["gemini"] = " ".join(cmd)

        rc, gem_out, gem_err = _run_capture_with_stdin(
            cmd, input_text=prompt_text, timeout=timeout_sec, cwd=cwd, env=child_env, step_name="gemini:run_stdin"
        )
        gem_out = gem_out or ""
        if rc != 0:
            return {"ok": False, "rc": rc, "diff_in": diff_in, "patch_out": "", "applied": False,
                    "rej_hints": (gem_out or gem_err)[:800], "patch_path": "", "temp_files": temp_files,
                    "steps": steps, "diagnostics": diag}

        cleaned = [ln for ln in gem_out.splitlines() if not ln.strip().startswith("```")]
        patch_out = "\n".join(cleaned).strip()
        if not patch_out:
            return {"ok": False, "rc": 4, "diff_in": diff_in, "patch_out": "", "applied": False,
                    "rej_hints": "Empty patch from model.", "patch_path": "", "temp_files": temp_files,
                    "steps": steps, "diagnostics": diag}

        diag["lengths"]["diff_in"] = len(diff_in)
        diag["lengths"]["patch_out"] = len(patch_out)
        diag["patch_head"] = "\n".join(patch_out.splitlines()[:30])

    except Exception:
        return {"ok": False, "rc": 5, "diff_in": diff_in, "patch_out": "", "applied": False,
                "rej_hints": "gemini failed", "patch_path": "", "temp_files": temp_files,
                "steps": steps + [{"ts": _now(), "step": "gemini:exception", "error": traceback.format_exc()}],
                "diagnostics": diag}

    # 3) save patch ------------------------------------------------------------
    try:
        if save_dir:
            Path(save_dir).mkdir(parents=True, exist_ok=True)
            patch_path = str(Path(save_dir) / "gemini_patch.diff")
        else:
            patch_path = _write_temp("", suffix=".diff", tag="output_patch")
        Path(patch_path).write_text(patch_out, encoding="utf-8")
    except Exception:
        return {"ok": False, "rc": 6, "diff_in": diff_in, "patch_out": "", "applied": False,
                "rej_hints": "save failed", "patch_path": "", "temp_files": temp_files,
                "steps": steps + [{"ts": _now(), "step": "save:exception", "error": traceback.format_exc()}],
                "diagnostics": diag}

    # 4) validate --------------------------------------------------------------
    if validate_patch:
        rc_chk, out_chk, err_chk = _run_capture(["git", "apply", "--check", patch_path],
                                                timeout=timeout_sec, cwd=cwd, env=child_env, step_name="git:check")
        if rc_chk != 0:
            return {"ok": False, "rc": rc_chk, "diff_in": diff_in, "patch_out": patch_out, "applied": False,
                    "rej_hints": (out_chk or err_chk)[:800], "patch_path": patch_path, "temp_files": temp_files,
                    "steps": steps, "diagnostics": diag}

    # 5) apply -----------------------------------------------------------------
    applied, rej_hints = False, ""
    if apply_patch and not dry_run:
        rc_apply, out_apply, err_apply = _run_capture(["git", "apply", "--index", "--reject", patch_path],
                                                      timeout=timeout_sec, cwd=cwd, env=child_env, step_name="git:apply")
        applied = (rc_apply == 0)
        if not applied:
            rej_hints = (out_apply or err_apply)[:800]

    # cleanup temps (optional)
    if not keep_temps:
        for p in temp_files[:-1]:  # keep last output_patch for visibility
            try: Path(p).unlink(missing_ok=True)
            except Exception: pass

    return {
        "ok": True, "rc": 0,
        "diff_in": (diff_in or "")[:100000],
        "patch_out": (patch_out or "")[:100000],
        "applied": applied, "rej_hints": rej_hints,
        "patch_path": patch_path,
        "temp_files": temp_files, "steps": steps, "diagnostics": diag
    }
