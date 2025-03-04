import socket
import os

class WebServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Web server running on http://{self.host}:{self.port}")

    def handle_request(self, conn):
        request = conn.recv(1024).decode()
        if not request:
            conn.close()
            return
        
        request_line = request.split('\n')[0]
        path = request_line.split(' ')[1]
        
        if path == "/":
            path = "/index.html"
        
        file_path = os.path.join(os.path.dirname(__file__), path.strip("/"))
        
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                response_body = file.read()
            content_type = self.get_content_type(path)
            response_header = f"HTTP/1.1 200 OK\nContent-Type: {content_type}\n\n"
        else:
            response_body = b"404 Not Found"
            response_header = "HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\n"
        
        conn.sendall(response_header.encode() + response_body)
        conn.close()

    def get_content_type(self, path):
        if path.endswith(".html"):
            return "text/html"
        elif path.endswith(".css"):
            return "text/css"
        elif path.endswith(".gif"):
            return "image/gif"
        else:
            return "application/octet-stream"

    def start(self):
        while True:
            conn, _ = self.server.accept()
            self.handle_request(conn)

if __name__ == "__main__":
    server = WebServer("192.168.254.108", 8080)
    server.start()
