import logging


def init_db_container():
    #
    container, name, pwd, port = ensure_load_config()
    data_dir = ensure_prepare_data_dir(container)
    docker_cmd = ensure_docker_env()
    ensure_launch_container(docker_cmd, container, name, pwd, port, data_dir)
    ensure_create_table()

    import socket, time
    host = get_pk_qc_mode_toml("db_host", "127.0.0.1")
    port = int(get_pk_qc_mode_toml("db_port", "3306"))
    for i in range(10):
        try:
            with socket.create_connection((host, port), timeout=5):
                logging.debug(f"MariaDB reachable at {host}:{port}")
                break
        except Exception as e:
            logging.debug(f"Waiting for MariaDB... ({i + 1}/10)")
            time.sleep(2)
    else:
        raise RuntimeError(f"MariaDB not reachable at {host}:{port}")
