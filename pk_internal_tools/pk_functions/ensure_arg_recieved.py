from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

@ensure_seconds_measured
def ensure_arg_recieved():
    """
    Receive selection via either argv or stdin.
      - argv:  python "{F_ENSURE_ARG_RECIEVED}" --sel "{{}}"
      - stdin: echo {{}} | python "{F_ENSURE_ARG_RECIEVED}" --from-stdin
    This function supports both.
    """
    # Lazy imports to avoid circular/import-time overhead
    import argparse
    import logging
    import sys
    import traceback

    from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

    try:
        args, unknown = _parse_args_safe(sys.argv[1:])
        if unknown:
            logging.debug("unknown argv tokens ignored: %r", unknown)

        target = _read_input(args)

        if args.echo:
            # print for CLI pipelines; also show GUI for quick visual check
            print(target)
            try:
                alert_as_gui(
                    title_="Received Payload",
                    ment=target,
                    auto_click_positive_btn_after_seconds=5,
                    input_text_default="",
                )
            except Exception:
                # GUI might not be available in headless; ignore
                pass
            return

        # If you want to open the path automatically, uncomment:
        # _open_path(target)

    except Exception:
        ensure_debug_loged_verbose(traceback)
    finally:
        pass


def _parse_args_safe(argv):
    """Parse args without exiting on errors; return (args, unknown)."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="ensure_arg_recieved",
        add_help=True,
        exit_on_error=False,  # prevent SystemExit on parse errors (Py3.9+)
        description="Receive selection via --sel or --from-stdin",
    )
    parser.add_argument("--sel", default="", help="Selection passed as argv")
    parser.add_argument("--from-stdin", dest="from_stdin", action="store_true",
                        help="Read selection from stdin instead of --sel")
    parser.add_argument("--query", default="", help="Optional query text (if you want to pass it)")
    parser.add_argument("--echo", action="store_true", help="Debug: print final string only")

    # Never raise on unknown flags; keep going
    args, unknown = parser.parse_known_args(argv)
    return args, unknown


def _strip_number_prefix(s: str) -> str:
    """Remove prefixes like '1. ', '12) ', '3- ' at the start of the line."""
    import re
    return re.sub(r'^\s*\d+[\.\)\-]\s*', '', s)


def _read_input(args) -> str:
    """Return effective payload from stdin or --sel, cleaned up."""
    import sys

    if getattr(args, "from_stdin", False):
        data = sys.stdin.read()
    else:
        data = args.sel or ""

    # normalize quotes/newlines and strip numeric prefixes like "1. "
    data = (data or "").strip().strip('"').strip("'")
    return _strip_number_prefix(data)


def _open_path(pth: str) -> None:
    """Open a path/URL with the default handler, cross-platform."""
    import os
    import platform
    import subprocess
    if not pth:
        return
    try:
        if os.name == "nt":  # Windows
            os.startfile(pth)  # type: ignore[attr-defined]
        else:
            sysname = platform.system().lower()
            if sysname == "darwin":
                subprocess.run(["open", pth], check=False)
            else:
                # Linux / WSL
                try:
                    subprocess.run(["wslview", pth], check=False)
                except Exception:
                    subprocess.run(["xdg-open", pth], check=False)
    except Exception as e:
        import logging
        logging.error("open failed: %s", e)
