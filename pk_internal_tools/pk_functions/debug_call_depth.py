def debug_call_depth(func_n):
    import inspect

    depth = len(inspect.stack(0))
    logging.debug(f" CALL DEPTH ({func_n}): {depth}")
    return depth
