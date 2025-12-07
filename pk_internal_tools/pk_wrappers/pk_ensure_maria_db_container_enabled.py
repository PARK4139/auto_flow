import os
import subprocess
import sys
import time
import traceback

from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.get_pk_qc_mode_toml import get_pk_qc_mode_toml
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root


# from pk_internal_tools.pk_objects.500_live_logic import get_pk_qc_mode_toml
# , '{PkTexts.TRY_GUIDE}', d_pk_system, '[ UNIT TEST EXCEPTION DISCOVERED ]'
# , print_red


CONTAINER = get_pk_qc_mode_toml("db_container_name", "nyaa_mariadb")
IMAGE = get_pk_qc_mode_toml("db_image", "mariadb:10.6")
DB_NAME = get_pk_qc_mode_toml("db_name", "nyaa_db")
DB_USER = get_pk_qc_mode_toml("db_user", "root")
DB_PASSWORD = get_pk_qc_mode_toml("db_password", "example")
DB_PORT = int(get_pk_qc_mode_toml("db_port", "3306"))
DATA_DIR = os.path.expanduser(get_pk_qc_mode_toml("db_data_dir", "~/nyaa_mariadb_data"))
lDB_HOST = get_pk_qc_mode_toml("db_host", "127.0.0.1")


def log(msg):
    print(f"[DB-SETUP] {msg}")


def container_exists():
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    return CONTAINER in result.stdout.splitlines()


def container_running():
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    return CONTAINER in result.stdout.splitlines()


def run_container():
    log("Starting new MariaDB container...")
    os.makedirs(DATA_DIR, exist_ok=True)
    subprocess.run([
        "docker", "run", "-d",
        "--name", CONTAINER,
        "-e", f"MYSQL_ROOT_PASSWORD={DB_PASSWORD}",
        "-e", f"MYSQL_DATABASE={DB_NAME}",
        "-p", f"{DB_PORT}:3306",
        "-v", f"{DATA_DIR}:/var/lib/mysql",
        IMAGE
    ], check=True)


def start_container():
    log("Starting stopped MariaDB container...")
    subprocess.run(["docker", "start", CONTAINER], check=True)


def wait_for_db():
    log("Waiting for MariaDB to be available...")
    for _ in range(15):
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1", user=DB_USER,
                password=DB_PASSWORD, database=DB_NAME, port=DB_PORT
            )
            conn.close()
            log("MariaDB is up and running!")
            return True
        except mysql.connector.Error:
            time.sleep(2)
    log("Failed to connect to MariaDB.")
    return False


def ensure_table():
    log("Ensuring nyaa_magnets table exists...")
    conn = mysql.connector.connect(
        host="127.0.0.1", user=DB_USER,
        password=DB_PASSWORD, database=DB_NAME, port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS nyaa_magnets (
      id INT AUTO_INCREMENT PRIMARY KEY,
      magnet TEXT UNIQUE,
      title VARCHAR(255),
      loaded TINYINT(1) DEFAULT 0,
      collected_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB CHARSET=utf8mb4;
    """)
    conn.commit()
    cur.close()
    conn.close()
    log("Table ensured.")


if __name__ == "__main__":
    try:
        # TODO
        ensure_pk_colorama_initialized_once()

        log("Checking Docker daemon...")
        try:
            subprocess.run(["docker", "info"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print("Docker daemon is not running! Please start Docker first.")
            sys.exit(1)

        if not container_exists():
            log("MariaDB container does not exist. Creating...")
            subprocess.run(["docker", "pull", IMAGE], check=True)
            run_container()
        else:
            if not container_running():
                start_container()
            else:
                log("MariaDB container already running.")
        if wait_for_db():
            ensure_table()
        else:
            sys.exit(1)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
