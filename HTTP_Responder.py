#!/usr/bin/python3

# Test calls
# GET
#   curl 127.0.0.1:8000/?param1=value1&param2=value2
# POST
#   curl -d "param1=value1&param2=value2" -X POST 127.0.0.1:8000

from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('------------GET-----------')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        headers = self.headers
        content_length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(content_length)
        print(headers, data)
        response = f""
        self.wfile.write(response.encode())

    def do_POST(self):
        print('------------POST-----------')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        headers = self.headers
        content_length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(content_length)
        print(headers, data)
        response = f""
        self.wfile.write(response.encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()
