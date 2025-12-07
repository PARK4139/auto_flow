def debug_current_threads(verbose: bool = True) -> list:
    """
    Print and return current alive threads.

    Args:
        verbose (bool): If True, prints detailed info.

    Returns:
        list: List of thread names.
    """
    import threading

    thread_list = threading.enumerate()

    if verbose:
        logging.info(f"Active thread count: {len(thread_list)}")
        for t in thread_list:
            print(f"  - name={t.name}, daemon={t.daemon}, alive={t.is_alive()}, ident={t.ident}")

    return [t.name for t in thread_list]


