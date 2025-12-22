def ensure_pk_exit_silent( os=None):
    import sys
    sys.stdout.flush()
    sys.stderr.flush()
    try:
        os._exit(0)  # Silent and immediate exit (no cleanup)
    except Exception as e:
        sys.exit(0)  # Fallback: graceful exit
