from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_headless_mode_requests_processed(
    prompts,
    work_mode="stream",           # "stream" | "capture" | "parallel"
    max_workers=4,                # used only for parallel
    timeout_sec=600,              # per task timeout
    save_dir=None,                # if set, save each stdout to a file
    as_json=False                 # use "--output json" instead of "text"
):
    """
    Fast Gemini CLI runner with work modes:
      - stream  : live stream (stdout/stderr -> logger), also returns collected text
      - capture : no live stream; capture stdout/stderr and return (fast & clean)
      - parallel: run multiple prompts concurrently (capture mode internally)

    Return: list of dicts per prompt:
      { "prompt": <str or file>, "rc": int, "ok": bool, "stdout": str, "stderr": str, "outfile": str|None }
    """
    # lazy imports
    import os
    import sys
    import tempfile
    import subprocess
    import threading
    import logging
    import traceback
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from pathlib import Path

    # ------------------------------ utils ------------------------------------

    def _ensure_iterable(obj):
        if obj is None:
            return []
        if isinstance(obj, (list, tuple)):
            return list(obj)
        return [obj]

    def _prep_prompt_arg(prompt_text: str):
        """
        If the prompt is long or multiline, write it to a temp file and pass the file path to gemini.
        This avoids quoting issues and is faster for large content.
        """
        s = str(prompt_text) if prompt_text is not None else ""
        if ("\n" in s) or (len(s) > 2000):  # heuristic threshold
            tmp = tempfile.NamedTemporaryFile(prefix="gemini_", suffix=".txt", delete=False)
            tmp.write(s.encode("utf-8", errors="ignore"))
            tmp.flush()
            tmp.close()
            return tmp.name, True
        return s, False

    def _build_gemini_cmd(prompt_arg: str, use_json: bool):
        """
        Build a cross-platform arg list for gemini CLI.
        """
        gemini_exe = os.environ.get("GEMINI_CMD", "gemini")
        output_fmt = "json" if use_json else "text"
        # Note: if prompt_arg is a file path, gemini treats it as input file.
        return [gemini_exe, "--stream", "--output", output_fmt, str(prompt_arg)]

    def _stream_subprocess(cmd_args, timeout=None, prefix=None):
        """
        Stream STDOUT/STDERR to logger in real-time and also collect them.
        """
        proc = subprocess.Popen(
            cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        stdout_lines, stderr_lines = [], []

        def _pump(stream, collector, level=logging.INFO, name="OUT"):
            for line in iter(stream.readline, ''):
                collector.append(line)
                if prefix:
                    logging.log(level, f"[{prefix}:{name}] {line.rstrip()}")
                else:
                    logging.log(level, line.rstrip())
            stream.close()

        t_out = threading.Thread(target=_pump, args=(proc.stdout, stdout_lines, logging.INFO, "OUT"), daemon=True)
        t_err = threading.Thread(target=_pump, args=(proc.stderr, stderr_lines, logging.WARNING, "ERR"), daemon=True)
        t_out.start(); t_err.start()

        try:
            rc = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            rc = proc.wait()
            logging.warning("[gemini] Process timed out and was killed.")

        t_out.join(); t_err.join()
        return rc, ''.join(stdout_lines), ''.join(stderr_lines)

    def _run_capture(cmd_args, timeout=None):
        """
        Run without streaming; capture stdout/stderr.
        """
        try:
            out = subprocess.check_output(cmd_args, stderr=subprocess.STDOUT, text=True, timeout=timeout)
            return 0, out, ""
        except subprocess.CalledProcessError as e:
            return e.returncode, e.output or "", ""
        except subprocess.TimeoutExpired as e:
            return 124, e.output or "", "TIMEOUT"

    def _handle_one(idx, prompt_text, mode, use_json):
        """
        Execute one prompt according to the chosen mode.
        """
        prompt_arg, is_file = _prep_prompt_arg(prompt_text)
        cmd = _build_gemini_cmd(prompt_arg, use_json=use_json)

        if mode == "stream":
            logging.info(f"[gemini] Running (stream) #{idx}: {cmd}")
            rc, out, err = _stream_subprocess(cmd, timeout=timeout_sec, prefix=f"{idx}")
        else:
            # capture & parallel share the same capture runner
            logging.info(f"[gemini] Running (capture) #{idx}: {cmd}")
            rc, out, err = _run_capture(cmd, timeout=timeout_sec)

        ok = (rc == 0)

        # optionally save output to file
        outfile = None
        if save_dir:
            Path(save_dir).mkdir(parents=True, exist_ok=True)
            suffix = ".json" if use_json else ".txt"
            outfile = str(Path(save_dir) / f"gemini_{idx:03d}{suffix}")
            try:
                Path(outfile).write_text(out, encoding="utf-8")
            except Exception as e:
                logging.warning(f"[gemini] failed to write outfile: {outfile}")

        # For capture/parallel, print summary after completion (not line-by-line)
        if mode != "stream":
            if ok:
                logging.info(f"[gemini] #{idx} OK, {len(out)} chars")
            else:
                logging.warning(f"[gemini] #{idx} FAIL rc={rc}")
                if err:
                    logging.warning(f"[gemini] #{idx} stderr: {err[:400]}")

        # cleanup temp file if we created one
        if is_file:
            try:
                os.unlink(prompt_arg)
            except Exception as e:
                pass

        return {
            "prompt": prompt_text,
            "rc": rc,
            "ok": ok,
            "stdout": out,
            "stderr": err,
            "outfile": outfile,
        }

    # ------------------------------ main -------------------------------------

    results = []
    try:
        prompts = _ensure_iterable(prompts)
        if not prompts:
            logging.info("[gemini] No prompts given.")
            return []

        n = len(prompts)
        logging.info(f"[gemini] {n} prompt(s); mode={work_mode}, json={as_json}")

        if work_mode == "parallel" and n > 1:
            # Run concurrently (capture mode internally)
            with ThreadPoolExecutor(max_workers=max_workers) as ex:
                fut_map = {ex.submit(_handle_one, i + 1, p, "capture", as_json): (i, p) for i, p in enumerate(prompts)}
                for fut in as_completed(fut_map):
                    res = fut.result()
                    results.append(res)
            # Preserve original order in results
            results.sort(key=lambda d: prompts.index(d["prompt"]))
        else:
            # stream or capture (sequential)
            mode = "stream" if work_mode == "stream" else "capture"
            for i, p in enumerate(prompts, start=1):
                res = _handle_one(i, p, mode, as_json)
                results.append(res)

        return results

    except Exception as e:
        logging.error(f"[gemini] crashed:\n{traceback.format_exc()}")
        return results
