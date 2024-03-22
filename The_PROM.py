#!/usr/bin/python3

# HTB Cyber Apocalypse 2024 - The Prom
# AT28C16 EEPROMs

from pwn import *
#context.log_level = 'debug'
LOW="0"
HIGH="5"
HIGHER="12" # Applied to pin A9 to read Device Identification reserved memory

io = remote('127.0.0.1', 4444)
#io.sendlineafter(b"> ", "help".encode('ascii'))
io.sendlineafter(b"> ", ("set_ce_pin("+LOW+")").encode('ascii')) # Chip Enabled (Power ON) - Enabled at 0V (active LOW)
io.sendlineafter(b"> ", ("set_oe_pin("+LOW+")").encode('ascii')) # Output Enable (Read Mode) - Enabled at 0V (active LOW)
io.sendlineafter(b"> ", ("set_we_pin("+HIGH+")").encode('ascii')) # Write Enable (Write Mode) - Disabled at 5V (active LOW)
#io.sendlineafter(b"> ", "set_io_pins([0, 0, 0, 0, 0, 0, 0, 0])".encode('ascii')) - For writing only

for i in range(int("7E0", 16), int("7FF", 16)):
    binary = str(bin(i)[2:]).rjust(11,"0")
    binary = binary.replace("1", HIGH)
    bits = list(binary)
    bits[1] = HIGHER # Pin A9

    received = io.recvuntil(b"> ")
    print(str(received)[3:-1])
    io.sendline(("set_address_pins(" + str(bits) + ")").encode('ascii'))
    
    received = io.recvuntil(b"> ")
    print(received.decode())
    io.sendline("read_byte()".encode('ascii'))

print(io.recv().decode())
io.close()

#io.interactive()
exit()

