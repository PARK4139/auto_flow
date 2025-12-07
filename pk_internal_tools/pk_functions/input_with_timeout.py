

def input_with_timeout(text_working: str, timeout_secs: int = 9999) -> str | None:
    import sys
    import threading
    from queue import Queue, Empty

    print(text_working, end=" ", flush=True)
    input_queue = Queue()

    def read_input():
        user_input = sys.stdin.readline()
        input_queue.put(user_input.strip())

    input_thread = threading.Thread(target=read_input, daemon=True)
    input_thread.start()

    try:
        return input_queue.get(timeout=timeout_secs)
    except Empty:
        return None
