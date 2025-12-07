import logging


def get_db_conn():
    #
    from mysql.connector import connect, Error

    import time
    host = get_pk_qc_mode_toml("db_host", "127.0.0.1")
    user = get_pk_qc_mode_toml("db_user", "root")
    pwd = get_pk_qc_mode_toml("db_password", "example")
    db = get_pk_qc_mode_toml("db_name", "nyaa_db")
    port = int(get_pk_qc_mode_toml("db_port", "3306"))
    for attempt in range(1, 6):
        try:
            logging.debug(f"Connecting to DB (attempt {attempt})...")
            conn = connect(host=host, user=user, password=pwd, database=db, port=port, charset="utf8mb4")
            logging.debug("DB connected")
            return conn
        except Error as e:
            logging.debug(f"Connection failed: {e}")
            time.sleep(5)
    raise RuntimeError("Could not connect to MariaDB after several attempts")
