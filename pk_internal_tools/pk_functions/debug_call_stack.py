def debug_call_stack():
    print("[CALL STACK]")
    for frame in inspect.stack()[1:5]:
        print(f"  - {frame.function} @ {frame.filename}:{frame.lineno}")


