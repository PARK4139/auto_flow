def is_internet_connected_2025_10_10():
    import socket
    try:
        socket.create_connection(("www.google.com", 80), timeout=2)
        return True
    except OSError:
        return False