#!/usr/bin/python3

from pwn import *
from tabulate import tabulate
import platform
import os
import stat
import argparse
import subprocess

# Parsing arguments
parser = argparse.ArgumentParser(description="Quick ELF proprieties and protection checker for Reverse Engineering and Binary Exploitation (https://github.com/davift/ctf)")
parser.add_argument('file', type=str, help="binary file")
parser.add_argument('-all', action='store_true', help="combine all outputs")
parser.add_argument('-fun', action='store_true', help="list functions")
parser.add_argument('-rw', action='store_true', help="list readeable + writeables")
parser.add_argument('-str', action='store_true', help="list strings")
parser.add_argument('-gad', action='store_true', help="list gadgets")
args = parser.parse_args()

# System attributes
if platform.machine() == 'x86_64':
    processor = 'amd64'
elif platform.machine() == 'i386' or platform.machine() == 'i686':
    processor = 'i386'
elif platform.machine() == 'arm':
    processor = 'arm'
elif 'aarch' in platform.machine() or 'aarch' in platform.machine():
    processor = 'arm64'
else:
    processor = 'other'

# Emojis
happy = '\U0001f60E '
unhappy = '\U0001f92c '

# Binary
executable = args.file
elf = ELF(executable, checksec= False)

# Binary attributes
attibutes = [
    [executable, elf.os, elf.elftype],
]

# Marking binary as executable
if elf.elftype == 'EXEC' or elf.elftype == 'DYN':
    st = os.stat(executable)
    os.chmod(executable, st.st_mode | stat.S_IEXEC)

# Binary parameters
parameters = [
    ['Native', elf.native, unhappy + "Might NOT run on this system" if not elf.native else happy + "Ready to run!"],
    ['Architecture', elf.arch.upper() + ' (' + str(elf.bits) + ' bits)', unhappy + "Different architectures: " + processor if elf.arch != processor else happy + "Perfect match!"],    ['Endianness', elf.endian.upper(), unhappy + "Use pack/unpack order the bytes" if elf.endian == 'little' else happy + "Bytes are ordered straightforward"],
    ['Dynamic Linked', elf.statically_linked, unhappy + "Addresses are randomized" if elf.statically_linked else happy + "Known addresses"],
    ['Stripped', elf.get_section_by_name('.symtab') is None, unhappy + "Debugging will be challenging" if elf.get_section_by_name('.symtab') is None else happy + "Easy peasy to debug"],
    ['UPX Packed', elf.packed, unhappy + "Hard to revser engineer" if elf.packed else happy + "No problem at all"],
]

# Binary protections
protections = [
    ['PIE Enabled', elf.pie, unhappy + "Randomized addresses in memory" if elf.pie else happy + "Static addresses in memory"],
    ['ASLR Enabled', elf.aslr, unhappy + "Randomized base addresses" if elf.aslr else happy + "Static base addresses"],
    ['NX Enabled', elf.nx, unhappy + "Shell-code is NOT allowed" if elf.nx else happy + "Let's execute shell-code"],
    ['Canary Enabled', elf.canary, unhappy + "Buffer overflow protection enabled" if elf.canary else happy + "Let's overflow"],
    ['RELRO Level', elf.relro, unhappy + "NO arbitrary overwrite allowed" if elf.relro == 'Full' else happy + "Let's overwrite arbitrarily"],
    ['Fortify Enabled', elf.fortify, unhappy + "Additional checks and protections enabled" if elf.fortify else happy + "All good!"],
]

# Linked libraries
libs = []
for key, value in elf.libs.items():
    libs.append({'Files': key, 'Base': hex(value)})

# Listing functions
funcs = []
for key, value in elf.functions.items():
    funcs.append({'Functions': key, 'Address': hex(value.address)})

# Listing GOT
got = []
for key, value in elf.got.items():
    got.append({'GOT': key, 'Value': hex(value)})

# Listing GOT
plt = []
for key, value in elf.plt.items():
    plt.append({'PLT': key, 'Value': hex(value)})

sections = []
# Listing writeable sections
for section in elf.sections:
    if section.header.sh_flags & 0x4 and section.header.sh_flags & 0x2:
        sections.append({'Section': section.name, 'Address': hex(section.header.sh_addr), 'Size': hex(section.header.sh_size)})

segments = []
# Listing writeable segments
for segment in elf.segments:
    if segment.header.p_flags & 0x4 and segment.header.p_flags & 0x2:
        segments.append({'Segment': hex(segment.header.p_vaddr), 'Size': hex(segment.header.p_memsz)})

strings = []
# Listing strings
strings_output = subprocess.run(['strings', '-tx', args.file], capture_output=True, text=True).stdout.split("\n")[:-1]
for string in strings_output:
    strings.append({'String': string.split()[1], 'Address': '0x' + string.split()[0]})

gadgets = []
# Listing gadgets
gadgets_output = subprocess.run(['ROPgadget', '--binary', 'badchars'], capture_output=True, text=True).stdout.split("\n")[2:-3]
for gadget in gadgets_output:
    gadgets.append({'Gadget': gadget.split(' : ')[1], 'Address': gadget.split(' : ')[0]})

# Building summary
summary = [
    {'Items': 'Functions', 'Qty': len(elf.functions.items())}, 
    {'Items': 'GOT', 'Qty': len(elf.got.items())}, 
    {'Items': 'PLT', 'Qty': len(elf.plt.items())}, 
    {'Items': 'RW Sections', 'Qty': len(sections)}, 
    {'Items': 'RW Segments', 'Qty': len(segments)},
    {'Items': 'Strings', 'Qty': len(strings)}, 
    {'Items': 'Gadgets', 'Qty': len(gadgets)},
]


# Printing header
print(tabulate(attibutes, headers=['File', 'O.S.', 'Type'], tablefmt="fancy_grid"))

# Printing option
if (not args.fun and not args.rw and not args.str and not args.gad) or (args.all):
    # No option
    print(tabulate(parameters, headers=['Parameters', 'Value', 'Comments'], tablefmt="fancy_grid"))
    print(tabulate(protections, headers=['Protections', 'Value', 'Comments'], tablefmt="fancy_grid"))
    print(tabulate(summary, headers='keys', tablefmt="fancy_grid"))
    # Combining all outputs
    if args.all:
        args.fun = True
        args.rw = True
        args.str = True
        args.gad = True
if args.fun:
    # Option function
    print(tabulate(libs, headers='keys', tablefmt="fancy_grid"))
    if funcs:
        print(tabulate(funcs, headers='keys', tablefmt="fancy_grid"))
    else:
        print("No DWARF symbols to determine function names.")
    print(tabulate(got, headers='keys', tablefmt="fancy_grid"))
    print(tabulate(plt, headers='keys', tablefmt="fancy_grid"))
if args.rw:
    # Option writeables
    print(tabulate(sections, headers='keys', tablefmt="fancy_grid"))
    print(tabulate(segments, headers='keys', tablefmt="fancy_grid"))
if args.str:
    # Option strings
    print(tabulate(strings, headers='keys', tablefmt="fancy_grid"))
if args.gad:
    # Option gadgets
    print(tabulate(gadgets, headers='keys', tablefmt="fancy_grid"))

exit()
