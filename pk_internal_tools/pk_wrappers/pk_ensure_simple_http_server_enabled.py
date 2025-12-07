import os
import socket
from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 8000
current_directory = os.getcwd()
print("현재 디렉토리 경로:", current_directory)
WORKING_DIRECTORY = current_directory
# WORKING_DIRECTORY = input("/원하는/경로")
WORKING_DIRECTORY = WORKING_DIRECTORY.strip()

os.chdir(WORKING_DIRECTORY)

# Get local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't have to be reachable
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# List serveable files
def list_files(directory):
    print("📄 Available files and directories:")
    for root, dirs, files in os.walk(directory):
        relative_root = os.path.relpath(root, directory)
        indent = '  ' * (relative_root.count(os.sep))
        for name in dirs:
            print(f"{indent}📁 {os.path.join(relative_root, name)}")
        for name in files:
            print(f"{indent}📄 {os.path.join(relative_root, name)}")
        break  # Only list top-level contents

handler = SimpleHTTPRequestHandler
httpd = HTTPServer(("", PORT), handler)

local_ip = get_local_ip()

print(f"\n📂 Serving HTTP from: {WORKING_DIRECTORY}")
print(f"🌐 Access from this machine: http://localhost:{PORT}")
print(f"📡 Access from other devices on the same network: http://{local_ip}:{PORT}\n")

list_files(WORKING_DIRECTORY)  # Show file list before starting server

httpd.serve_forever()
