#!/usr/bin/python3

# HTB Cyber Apocalypse 2024 - Stop Drop and Roll

import socket

host = '127.0.0.1'
port = 1337

import socket
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.connect( ( host, port ) )

while 1:
    data = s.recv(1024).decode()
    print(data)
    if data.find("Are you ready?") != -1:
        answer = "y\n"
        s.send(answer.encode())
        print(answer)
        break

while 1:
    data = s.recv(1024).decode()

    if (data.find("GORGE") != -1 or data.find("PHREAK") != -1 or data.find("FIRE") != -1):
        lines = data.split("\n")
        print(lines[0])
        answer = "-".join(lines[0].split(', ')).replace("GORGE", "STOP").replace("PHREAK", "DROP").replace("FIRE", "ROLL") + "\n"
        print(answer)
        s.send(answer.encode())
        
    elif data.find("What do you do?") != -1:
        continue

    elif data.find("Unfortunate! You died!") != -1:
        print(data)
        print('FAILED!')
        break

    elif data.find("HTB{") != -1:
        print('PWNED! ' + data)
        break

s.close()
