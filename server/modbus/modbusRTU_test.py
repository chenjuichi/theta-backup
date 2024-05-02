from pymodbus.client.serial import ModbusSerialClient as ModbusClient

import threading
import time
import signal
import keyboard

import socket

import sys

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

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.32.182', 9701))  # IP 地址

### init
client = ModbusClient(method='rtu', port='COM6', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)
connectOK=client.connect()
print("connect... ", connectOK)

### open蜂鳴器響聲
coin_rq = client.write_coil(slave=_SLAVE_ID, address=_ADDR_BEEP_ENABLE, value=1)
print("open beep... ", coin_rq)

###rf_enable
coin_rq = client.write_coil(slave=_SLAVE_ID, address=_ADDR_RF_ENABLE, value=1)
print("rf_enable... ", coin_rq)

#-----------------------------

def polling_hdg_06(arg):
  #t = threading.currentThread()
  print("Hello HDG-06...")
  print("chip polling...")
  while getattr(threading.currentThread(), "do_run", True):   #stopping threading by a "do_run" flag.
    #read Input Register (InReg), address=0
    tmp = client.read_input_registers(slave=_SLAVE_ID, address=_ADDR_SYS_FLAG, count=1)
    #delay over 1000ms
    #time.sleep(0.5)
    time.sleep(1)
    new_chip=tmp.registers[0] & 0x0003
    #if not tmp.isError():
    #  if new_chip==2 or new_chip==3:
    if (not tmp.isError()) and (new_chip==2 or new_chip==3):
        print('\n'+'new_chip_flag: ' + '\033[42m' + str(new_chip) + '\033[0m')

        #read Input Register (InReg), address=1 ~ 4
        tmp_uids = client.read_input_registers(slave=_SLAVE_ID, address=_ADDR_UID, count=4)
        myList=tmp_uids.registers

        uid_info=[]
        for uid in myList:
          #print("uid: ", uid)
          uid_info.append((uid & 0x00FF))
          uid_info.append((uid >> 8))
        print("uid_info: ", uid_info)
        print(type(uid_info))
        byte_data = bytes(uid_info)                 # 将list轉換為字串組合
        #data_to_send = byte_data.decode('ascii')
        start_client(byte_data)
        #data_to_send = b'12345678'
        #client_socket.send(data_to_send)
        #client_socket.send(data_to_send)
        #print('送出資料為：', ascii_string)
        '''p
        try:
            # 将字节数组解码为字符串（使用 'utf-8' 编码）
            decoded_string = byte_data.decode('utf-8')
            print(decoded_string)
        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError: {e}")
        '''

        #read Input Register (InReg), address=5
        tmp_blk_info = client.read_input_registers(slave=_SLAVE_ID, address=_ADDR_BLOCK_INFO, count=1)
        chip_block_size = (tmp_blk_info.registers[0] & 0x00FF)
        chip_block_number = (tmp_blk_info.registers[0] >> 8)
        print("chip_block_size, chip_block_number: ", chip_block_size,"bytes,", chip_block_number, "blocks")

        #read Input Register (InReg), address=6
        tmp_uid_size = client.read_input_registers(slave=_SLAVE_ID, address=_ADDR_UID_SIZE, count=1)
        uid_size = (tmp_uid_size.registers[0] & 0x000F)
        print("uid_size: ", uid_size, "bytes")

    time.sleep(0.5)
    #time.sleep(1)

  print("Stopping hdg-06 task...")

  client.close()

#-----------------------------

def start_client(data_to_send):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.32.182', 9701))  # IP 地址

    # send data
    #data_to_send = b'12345678'
    client_socket.send(data_to_send)
    print('送出資料為：', data_to_send)

    # close connect
    client_socket.close()

#-----------------------------

def signal_handler(signal, frame):
    print("\nYou pressed Ctrl-C! Stopping the program...")
    #client_socket.close()
    sys.exit(0)

#-----------------------------

def main():
  signal.signal(signal.SIGINT, signal_handler)

  t = threading.Thread(target=polling_hdg_06, args=("hdg-06 task",))
  t.start()

  while True:
    print("run( press p to stop!)....")
    if keyboard.read_key() == "p":
      t.do_run = False
      t.join()  # 等待THREAD结束
      print("You pressed p to stop polling...")
      #client_socket.close()
      break
    time.sleep(1)
  #time.sleep(1)

  #start_client()
#-----------------------------

if __name__ == "__main__":
  main()

