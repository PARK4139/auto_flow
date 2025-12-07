import http.server

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 캐시 방지 헤더 추가
        self.send_header('Cache-Control', 'no-store')  # 캐시를 저장하지 않음
        self.send_header('Pragma', 'no-cache')  # HTTP 1.0 캐시 방지
        self.send_header('Expires', '0')  # 만료 시간을 0으로 설정
        super().end_headers()

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except ConnectionResetError:
            print("Connection reset by client. Ignoring...")

if __name__ == "__main__":
    server_address = ('', 9090)
    httpd = http.server.HTTPServer(server_address, NoCacheHTTPRequestHandler)
    print("Serving HTTP on port 9090...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server.")
        httpd.server_close()
