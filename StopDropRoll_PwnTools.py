#!/usr/bin/python3

# HTB Cyber Apocalypse 2024 - Stop Drop and Roll

from pwn import *

host = '127.0.0.1'
port = 1337

io = remote(host, port)

io.recvuntil(b"Are you ready? (y/n)")
io.sendline(b"y")
io.recvline()

while 1:
    data = str(io.recvline())
    print(data[2:-3])
    if (data.find("GORGE") != -1 or data.find("PHREAK") != -1 or data.find("FIRE") != -1):
        answer = "-".join(data[2:-3].split(', ')).replace("GORGE", "STOP").replace("PHREAK", "DROP").replace("FIRE", "ROLL")
        print(answer)
        io.recv()
        io.sendline(answer.encode('ascii'))
    elif data.find("Unfortunate! You died!") != -1:
        print("Unfortunate! You died!")
        exit()
    else:
        print('Pwned!')
        exit()

io.interactive()
exit()

