from http.server import BaseHTTPRequestHandler, HTTPServer

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("<h1>CI/CD działa 🚀</h1>".encode())

server = HTTPServer(("0.0.0.0", 8000), handler)
server.serve_forever()
