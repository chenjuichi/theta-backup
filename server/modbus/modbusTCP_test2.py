#from pymodbus.client.serial import ModbusSerialClient as ModbusClient
from pymodbus.client import ModbusTcpClient as ModbusClient
#from pyModbusTCP.client import ModbusClient

from pymodbus.exceptions import ModbusIOException, ConnectionException

import threading
import time

import keyboard

#-----------------------------
_SLAVE_ID = 1

_FLAG_CHIP_EXIST  = 0x01;
_FLAG_NEW_CHIP    = 0x02;
_FLAG_READ_DONE   = 0x04;
_FLAG_READ_ERROR  = 0x08;
_FLAG_WRITE_DONE  = 0x10;
_FLAG_WRITE_ERROR = 0x20;
_FLAG_ANT_ERROR   = 0x80;

_ADDR_RF_ENABLE      = 0x00;
_ADDR_READ_ENABLE    = 0x01;
_ADDR_WRITE_ENABLE   = 0x02;
_ADDR_BEEP_ENABLE    = 0x03;
_ADDR_CLEAR_FLAG_REG = 0x04

_ADDR_HAT_MODE = 0x0400;
_ADDR_FETCH_BLOCK_NUM = 0x0401;
_ADDR_RW_BLOCK_NUM    = 0x0402;

_ADDR_SYS_FLAG   = 0x00;
_ADDR_UID        = 0x01;
_ADDR_BLOCK_INFO = 0x05;
_ADDR_UID_SIZE   = 0x06;

_ADDR_HAT_MODE        = 0x0400;
_ADDR_FETCH_BLOCK_NUM = 0x0401;
_ADDR_RW_BLOCK_NUM    = 0x0402;
#-----------------------------

### init
#client = ModbusClient(method='rtu', port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)
#client = ModbusClient('192.168.43.101', port=502, unit=1)
#connectOK=client.connect()
#connectOK=client.open()
#print("connect... ", connectOK)

### open蜂鳴器響聲
try:
    # Create a Modbus TCP client instance
    client = ModbusClient('192.168.32.101', port=502, unit=1)

    # Connect to the Modbus server
    if client.connect():
        # Write a value of 1 to the specified coil
        client.write_coil(_ADDR_BEEP_ENABLE, 1, unit=_SLAVE_ID)
        print(f"Successfully wrote 1 to coil {_ADDR_BEEP_ENABLE} on slave {_SLAVE_ID}")

        # Read the value of the same coil to verify
        read_response = client.read_coils(_ADDR_BEEP_ENABLE, 1, unit=_SLAVE_ID)

        if not read_response.isError():
            # The read_response.bits[0] will contain the value of the coil
            if read_response.bits[0] == True:
                print("Write operation was successful.")
            else:
                print("Write operation failed.")
        else:
            print(f"Error reading coil {_ADDR_BEEP_ENABLE}: {read_response}")

    else:
        print("Failed to connect to Modbus server")

except ModbusIOException as e:
    print(f"Modbus IO Error: {str(e)}")
except ConnectionException as e:
    print(f"Connection Error: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the Modbus TCP client connection
    client.close()