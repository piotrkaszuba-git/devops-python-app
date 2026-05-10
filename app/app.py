import psycopg2
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_HOST = "db"
DB_NAME = "myapp"
DB_USER = "devops"
DB_PASS = "devops123"

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            conn.close()
            break
        except:
            print("Waiting for DB...")
            time.sleep(2)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_response(404)
            self.end_headers()
            return

        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS visits (count INT);")
        cur.execute("INSERT INTO visits (count) VALUES (1);")
        cur.execute("SELECT COUNT(*) FROM visits;")
        count = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(f"<h1>Visits: {count}</h1>".encode())

wait_for_db()

server = HTTPServer(("0.0.0.0", 8000), handler)
server.serve_forever()
