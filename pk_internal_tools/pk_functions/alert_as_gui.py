import json
import logging
import os
import platform
import socket
import subprocess
import sys
import threading  # For potential future use, not strictly needed for this version
import time

from pk_internal_tools.pk_objects.pk_files import F_UV_PYTHON_EXE

# --- IPC Client Setup ---
HOST = '127.0.0.1'
PORT = 50001  # Must match the port in flet_alert_server.py

# Global flag to track if server launch is in progress
flet_server_launch_in_progress = threading.Lock()


def send_ipc_command(command: str, data: dict = None):
    """Sends a command to the Flet IPC server and waits for a response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            message = {"command": command, "data": data if data is not None else {}}
            s.sendall(json.dumps(message).encode('utf-8'))

            response_data = s.recv(4096).decode('utf-8')
            response = json.loads(response_data)
            return response
        except ConnectionRefusedError:
            logging.error(f"IPC server not running at {HOST}:{PORT}. Please ensure flet_alert_server.py is running.")
            return {"status": "error", "message": "Server not running."}
        except Exception as e:
            logging.error(f"Error sending IPC command: {e}", exc_info=True)
            return {"status": "error", "message": f"IPC communication error: {e}"}


def launch_flet_server():
    """Launches the Flet alert server in the background."""
    with flet_server_launch_in_progress:  # Ensure only one launch attempt at a time
        logging.info("Attempting to launch Flet Alert Server...")
        flet_server_path = os.path.join(
            os.path.dirname(__file__),
            "flet_alert_server.py"
        )

        # Determine the correct Python executable for the virtual environment
        venv_python_executable = F_UV_PYTHON_EXE
        command = [
            venv_python_executable,
            flet_server_path
        ]

        logging.debug(f"Attempting to launch Flet server with executable: {venv_python_executable}")  # Add this line

        # Launch as a detached process (Windows specific for true background)
        # Using Popen with creationflags for Windows to detach
        if sys.platform == "win32":
            creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            # Redirect stdout and stderr to current process's stdout/stderr for debugging
            process = subprocess.Popen(command, creationflags=creationflags, close_fds=True, stdout=sys.stdout, stderr=sys.stderr)
        else:
            # For Linux/macOS, simply running in background with & or nohup
            process = subprocess.Popen(command, stdout=sys.stdout, stderr=sys.stderr, preexec_fn=os.setpgrp)

        logging.info(f"Flet Alert Server launched with PID: {process.pid}")

        # Wait for the server to become ready (retry connection)
        max_retries = 10
        for i in range(max_retries):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)  # Short timeout for connection attempt
                    s.connect((HOST, PORT))
                    logging.info("Flet Alert Server is ready.")
                    return True
            except (ConnectionRefusedError, socket.timeout):
                logging.debug(f"Waiting for Flet Alert Server... (Attempt {i + 1}/{max_retries})")
                time.sleep(1)  # Wait a bit before retrying
            except Exception as e:
                logging.error(f"Unexpected error while waiting for Flet server: {e}", exc_info=True)
                return False

        logging.error("Flet Alert Server did not become ready within the timeout.")
        return False


# --- Main alert_as_gui function ---
def alert_as_gui(title_: str, ment: str, auto_click_positive_btn_after_seconds: int, input_text_default: str = "", btn_list=None):
    if not btn_list:
        btn_list = ["확인"]

    if platform.system() == 'Windows':
        # Check if server is running, if not, launch it
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.1)  # Quick check
                s.connect((HOST, PORT))
                server_running = True
        except (ConnectionRefusedError, socket.timeout):
            server_running = False
        except Exception as e:
            logging.error(f"Error checking Flet server status: {e}", exc_info=True)
            server_running = False

        if not server_running:
            logging.info("Flet Alert Server not found. Launching it...")
            if not launch_flet_server():
                logging.error("Failed to launch Flet Alert Server. Cannot display alert.")
                return "Error", None

        # Send the show_alert command
        alert_data = {
            "title": title_,
            "ment": ment,
            "input_text_default": input_text_default,
            "btn_list": btn_list
        }
        response = send_ipc_command("show_alert", alert_data)

        if response.get("status") == "ok":
            result = response.get("result", {})
            btn_txt_clicked = result.get("button_clicked")
            input_value = result.get("input_value")
            txt_written = input_value if input_text_default != "" else None
            return btn_txt_clicked, txt_written
        else:
            logging.error(f"Flet Alert Server returned an error: {response.get('message', 'Unknown error')}")
            return "Error", None

    else:
        logging.debug(f"{ment}")
        return None, None  # Or a default value if needed
