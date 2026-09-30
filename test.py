from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.request
import json

WEBHOOK_URL = "https://discord.com/api/webhooks/1550538777750143106/7I4_j63iAPnp2zp23t5aEZ4-dEJVOi6l0VEX9RoviWuFA-LsVCsfuMCUdhSZFt3o80iC"

html_content = """
<!DOCTYPE html>
<html>
<head><title>...</title></head>
<body>
<script>
    fetch('""" + WEBHOOK_URL + """', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: 'hi' })
    });
</script>
</body>
</html>
"""

class SilentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    def log_message(self, format, *args):
        pass  # Hides console logs

def main():
    server = HTTPServer(('localhost', 8080), SilentHandler)
    print("Server running at http://localhost:8080")
    print("Open this URL in your browser.")
    server.serve_forever()

if __name__ == "__main__":
    main()
