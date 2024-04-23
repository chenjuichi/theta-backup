#from pymodbus.client.serial import ModbusSerialClient as ModbusClient
#from pymodbus.client.tcp import ModbusTcpClient as ModbusClient
from pyModbusTCP.client import ModbusClient

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
client = ModbusClient(host='192.168.32.101', port=502, unit_id=_SLAVE_ID)

connectOK=client.open()
print("connect... ", connectOK)

### open蜂鳴器響聲
#coin_rq = client.write_coil(slave=_SLAVE_ID, address=_ADDR_BEEP_ENABLE, value=1)
coin_rq = client.write_single_coil(_ADDR_BEEP_ENABLE, 1)
print("open beep... ", coin_rq)

###rf_enable
#coin_rq = client.write_coil(slave=_SLAVE_ID, address=_ADDR_RF_ENABLE, value=1)
coin_rq = client.write_single_coil(_ADDR_RF_ENABLE, 1)
print("rf_enable... ", coin_rq)

#-----------------------------

