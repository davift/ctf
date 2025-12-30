#!/usr/bin/env python3
import sys
from pymodbus.client import ModbusTcpClient

# Data Type             I/O Type            Access      Description
# Coils                 Digital outputs     Read/Write  1-bit values (True/False).
# Discrete Inputs       Digital inputs      Read Only   1-bit values (0/1).
# Holding Registers     Analogue outputs    Read/Write  16-bit integers (configuration and setpoints).
# Input Registers       Analogue inputs     Read Only   16-bit integers (measurements.

if len(sys.argv) < 2:
    print("Usage: python3 modbus-client.py <TARGET_IP>")
    sys.exit(1)


IP_ADDRESS = sys.argv[1]
PORT = 502
UNIT_ID = 1 # aka Server Address, bewcause there might be more than one in a network.

def get_client():
    client = ModbusTcpClient(IP_ADDRESS, port=PORT)
    if client.connect():
        print(f"[*] Connected to {IP_ADDRESS}")
        return client
    else:
        print(f"[!] Connection to {IP_ADDRESS} failed")
        exit(1)

def read_val(client, addr, is_coil=False):
    if is_coil:
        res = client.read_coils(address=addr, count=1, slave=UNIT_ID)
        return res.bits[0] if not res.isError() else None
    else:
        res = client.read_holding_registers(address=addr, count=1, slave=UNIT_ID)
        return res.registers[0] if not res.isError() else None

def write_val(client, addr, value, is_coil=False):
    if is_coil:
        res = client.write_coil(addr, value, slave=UNIT_ID)
    else:
        res = client.write_register(addr, value, slave=UNIT_ID)
    
    if not res.isError():
        print(f"[+] Successfully wrote {value} to {'Coil' if is_coil else 'HR'} {addr}")
    else:
        print(f"[!] Failed to write to address {addr}")

def main():
    client = get_client()

    try:
        # READ COIL
        C11 = read_val(client, 11, is_coil=True)
        print(f"\tC11\t{C11}")
        # READ HOLDING REGISTER
        HR0 = read_val(client, 0, is_coil=False)
        print(f"\tHR0\t{HR0}")

        # WRITE COIL
        write_val(client, 11, False, is_coil=True)
        # WRITE HOLDING REGISTER
        write_val(client, 0, 0, is_coil=False)

        # READ COIL
        C11 = read_val(client, 11, is_coil=True)
        print(f"\tC11\t{C11}")
        # READ HOLDING REGISTER
        HR0 = read_val(client, 0, is_coil=False)
        print(f"\tHR0\t{HR0}")


    finally:
        client.close()
        print("[*] Connection closed.")

if __name__ == "__main__":
    main()