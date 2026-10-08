from http.server import HTTPServer, BaseHTTPRequestHandler


class HealthCheckHandler(BaseHTTPRequestHandler):
    health_hits = 0

    def do_GET(self):
        # Проверяем, что запрос пришел именно на эндпоинт /health
        if self.path == '/health':
            HealthCheckHandler.health_hits += 1
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        elif self.path == '/metrics':
            body = f'health_hits {HealthCheckHandler.health_hits}'.encode()
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

def run():
    server_address = ('', 8080)  # Слушает на всех интерфейсах, порт 8080
    httpd = HTTPServer(server_address, HealthCheckHandler)
    print("Сервер запущен на порту 8080...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()