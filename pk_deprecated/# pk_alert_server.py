import json
import logging
import socket
import sys
import threading

import flet as ft

from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized

# --- IPC Server Setup ---
HOST = '127.0.0.1'
PORT = 50001  # Chosen port for IPC

# Global variables to manage the Flet page and dialog
flet_page_instance = None
current_dialog_future = None  # To hold a future for dialog results


def handle_client_connection(conn, addr):
    global flet_page_instance, current_dialog_future
    logging.info(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(4096).decode('utf-8')
            if not data:
                break

            request = json.loads(data)
            command = request.get("command")
            req_data = request.get("data", {})

            if command == "show_alert":
                logging.debug(f"Received show_alert command: {req_data}")
                if flet_page_instance:
                    # Use a Future to get the dialog result back to the server thread
                    current_dialog_future = threading.Event()
                    dialog_result = {}

                    def show_flet_dialog():
                        nonlocal dialog_result
                        title = req_data.get("title", "Alert")
                        ment = req_data.get("ment", "")
                        btn_list = req_data.get("btn_list", ["OK"])
                        input_text_default = req_data.get("input_text_default", "")

                        input_field = None
                        if input_text_default != "":
                            input_field = ft.TextField(label="Input", value=input_text_default, width=300)

                        def close_dialog_from_flet(e):
                            nonlocal dialog_result
                            clicked_button_text = e.control.text
                            input_value = input_field.value if input_field else ""
                            dialog_result = {"button_clicked": clicked_button_text, "input_value": input_value}
                            flet_page_instance.dialog.open = False
                            flet_page_instance.update()
                            current_dialog_future.set()

                        actions = [ft.TextButton(btn_text, on_click=close_dialog_from_flet) for btn_text in btn_list]

                        content_controls = [ft.Text(ment, color=ft.Colors.WHITE)]
                        if input_field:
                            content_controls.append(input_field)

                        flet_page_instance.dialog = ft.AlertDialog(
                            modal=True,
                            bgcolor=ft.Colors.BLUE_GREY_800,
                            title=ft.Text(title, color=ft.Colors.WHITE),
                            content=ft.Column(content_controls),
                            actions=actions,
                            actions_alignment=ft.MainAxisAlignment.CENTER,
                        )
                        flet_page_instance.dialog.open = True
                        flet_page_instance.update()

                    # Run Flet UI updates on the main Flet thread
                    show_flet_dialog()

                    # Wait for the dialog to be closed and result to be set
                    current_dialog_future.wait()
                    logging.debug(f"Dialog closed, dialog_result: {dialog_result}")
                    response = {"status": "ok", "result": dialog_result}
                else:
                    response = {"status": "error", "message": "Flet page not initialized."}
            else:
                response = {"status": "error", "message": "Unknown command."}

            logging.debug(f"Server constructing response: {response}")
            encoded_response = json.dumps(response).encode('utf-8')
            logging.debug(f"Server sending encoded response (bytes): {encoded_response}")
            conn.sendall(encoded_response)

    except ConnectionResetError:
        logging.warning(f"Client {addr} disconnected unexpectedly.")
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON received from {addr}: {data}")
    except Exception as e:
        logging.error(f"Error handling client {addr}: {e}", exc_info=True)
    finally:
        conn.close()
        logging.info(f"Connection with {addr} closed.")


def start_ipc_server():
    logging.info(f"Starting IPC server on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of address
        try:
            s.bind((HOST, PORT))
            s.listen()
            logging.info("IPC server listening...")
            while True:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=handle_client_connection, args=(conn, addr))
                client_thread.daemon = True  # Allow main program to exit even if thread is running
                client_thread.start()
        except OSError as e:
            logging.error(f"Could not bind to port {PORT}. Is another instance running? Error: {e}")
            # If bind fails, it means another instance is likely running or port is in use.
            # The Flet app should probably exit in this case.
            if flet_page_instance:
                flet_page_instance.run_sync(lambda: flet_page_instance.window_destroy())
                flet_page_instance.run_sync(lambda: flet_page_instance.app.exit())
            sys.exit(1)  # Exit if server cannot start
        except Exception as e:
            logging.error(f"IPC server error: {e}", exc_info=True)


def main(page: ft.Page):
    global flet_page_instance
    flet_page_instance = page  # Store the page instance globally

    page.title = "Flet Alert Server"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 1  # Make it very small, almost invisible
    page.window_height = 1
    page.window_always_on_top = False  # Don't need to be always on top for a background app
    page.window_bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.window_opacity = 0.0  # Make it completely invisible
    page.window_frameless = True  # No frame for invisible window

    # Start the IPC server in a separate thread
    server_thread = threading.Thread(target=start_ipc_server, daemon=True)
    server_thread.start()

    # Add a dummy control to keep the Flet app running
    page.add(ft.Container())
    page.update()


if __name__ == "__main__":
    ensure_pk_system_log_initialized(__file__)

    # Check if another instance is already running by trying to connect
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            s.sendall(json.dumps({"command": "ping"}).encode('utf-8'))  # Send a dummy command
            s.close()
            logging.info("Another Flet Alert Server instance is already running. Exiting this one.")
            sys.exit(0)  # Exit if another instance is found
        except ConnectionRefusedError:
            logging.info("No existing Flet Alert Server found. Starting new instance.")
            # Only start the Flet app if no other instance is running
            ft.app(target=main)
        except Exception as e:
            logging.error(f"Error checking for existing instance: {e}", exc_info=True)