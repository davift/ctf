#!/usr/bin/python3

import socket
import json

def send_raw_http_request(host, port, request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(request.encode())

    response = b""
    while True:
        recv_data = client_socket.recv(1024)
        if not recv_data:
            break
        response += recv_data

    client_socket.close()
    return response.decode()

domain = 'example.com'

request_body = { 'key': 'value' }
json_body = json.dumps(request_body)
length = len(json_body)

# It does not support HTTPS schema. No matter the port, it will a regular HTTP request.
response = send_raw_http_request('127.0.0.1', 8000, "POST / HTTP/1.1\r\nHost: " + domain + "\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Safari/537.36\r\nConnection: close\r\nContent-Type: application/json\r\nContent-Length: " + str(length) + "\r\n\r\n" + json_body + "\r\n")

print(response)
exit()
