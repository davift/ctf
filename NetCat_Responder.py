#!/usr/bin/python3

from pwn import *

def echo_server(host, port):
    server = listen(port=port, bindaddr=host)

    print(f"Listening on {host}:{port}...")

    while True:
        conn = server.wait_for_connection()
        with conn:
            try:
                while True:
                    # Send a prompt.
                    conn.send("> ".encode())

                    data = conn.recvline().decode().strip()

                    # Interrupt if empty line is received.
                    # if not data:
                    #     break

                    # Reflect the data received.
                    # conn.send((data + "\n").encode())

                    # Always repond with a prompt.
                    # conn.send("REPLY\n".encode())
            except EOFError:
                conn.close()
                exit()

HOST = '127.0.0.1'
PORT = 4444
echo_server(HOST, PORT)
