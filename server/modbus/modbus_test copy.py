#from pymodbus3.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.client.serial import ModbusSerialClient as ModbusClient
#from pymodbus.exceptions import ConnectionException      #非同步使用
#from pymodbus.register_read_message import ReadHoldingRegistersResponse

from threading import Timer
import time

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


### init
client = ModbusClient(method='rtu', port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)
connectOK=client.connect()
print("connect... ", connectOK)

### 清除Flag, 含 NEW_CHIP_FLAG, READ_DONE_ FLAG, READ_ERROR_ FLAG, WRITE_DONE_ FLAG, WRITE_ERROR_ FLAG
### 清除InReg, 含 UID, CHIP_BLOCK_SIZE, CHIP_BLOCK_NUM, UID_SIZE
#coin_rq = client.write_coil(_SLAVE_ID, _ADDR_CLEAR_FLAG_REG, 1)
#coin_rq = client.write_coil(slave=_SLAVE_ID, address=_ADDR_CLEAR_FLAG_REG, value=1)
#print("clear flag, InReg... ", coin_rq)

### open蜂鳴器響聲
#coin_rq = client.write_coil(_SLAVE_ID, _ADDR_BEEP_ENABLE, 1)
coin_rq = client.write_coil(slave=_SLAVE_ID, address=_ADDR_BEEP_ENABLE, value=1)
print("open beep... ", coin_rq)

###read_enable
##coin_rq = client.write_coil(_SLAVE_ID, _ADDR_READ_ENABLE, 1)
#coin_rq = client.write_coil(slave=_SLAVE_ID, address=_ADDR_READ_ENABLE, value=1)
#print("read_enable... ", coin_rq)

###write_enable
#coin_rq = client.write_coil(_SLAVE_ID, _ADDR_WRITE_ENABLE, 1)
#coin_rq = client.write_coil(slave=_SLAVE_ID, address=_ADDR_WRITE_ENABLE, value=1)
#print("write_enable... ", coin_rq)

###rf_enable
#coin_rq = client.write_coil(_SLAVE_ID, _ADDR_RF_ENABLE, 1)
coin_rq = client.write_coil(slave=_SLAVE_ID, address=_ADDR_RF_ENABLE, value=1)
print("rf_enable... ", coin_rq)

#fetchBlockNum = 0
#reg_rq=client.write_register(slave=_SLAVE_ID, address=_ADDR_FETCH_BLOCK_NUM, value=fetchBlockNum)
#if not reg_rq.isError():
#  print("FETCH_BLOCK_NUM... ", reg_rq, reg_rq.registers)
#else:
#  print("error: {}".format(reg_rq))

'''
###
tmp = client.read_holding_registers(slave=_SLAVE_ID, address=_ADDR_BLOCK_INFO, count=1)
if not tmp.isError():
  chip_block_size = (tmp.registers[0] & 0X00FF)
  chip_block_num  = (tmp.registers[0] & 0XFF00)
  print("read_holding_registers... ", tmp, tmp.registers)
  print("CHIP_BLOCK_SIZE: ", chip_block_size)
  print("CHIP_BLOCK_NUM: ", chip_block_num)
else:
  print("error: {}".format(tmp))
#time.sleep(0.5)
'''
print("Hello HDG-06...")
print("chip polling...")
while True:
  #read Input Register (InReg), address=0
  tmp = client.read_input_registers(slave=_SLAVE_ID, address=_ADDR_SYS_FLAG, count=1)
  #delay over 300ms
  time.sleep(0.5)
  new_chip=tmp.registers[0] & 0x0003
  if not tmp.isError():
    #print("Hello HDG-06...")
    if new_chip==2 or new_chip==3:
      print('\n'+'new_chip_flag: ' + '\033[42m' + str(new_chip) + '\033[0m')
    #else:
    #  print("new_chip_flag: "+ str(new_chip) + '\n')

      #read Input Register (InReg), address=1 ~ 4
      tmp_uids = client.read_input_registers(slave=_SLAVE_ID, address=_ADDR_UID, count=4)
      myList=tmp_uids.registers
      #print("uids: ", tmp_uid, myList)
      uid_info=[]
      for uid in myList:
        #print("uid: ", uid)
        uid_info.append((uid & 0x00FF))
        uid_info.append((uid >> 8))
      print("uid_info: ", uid_info)

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


'''
#i = 0
#while i < 1:
  #t = Timer(0.5, checkNewChipFlag) # 在5秒後，自動執行 hello()
  #t.start()
  #checkNewChipFlag # 在5秒後，自動執行 hello()
  #time.sleep(2)

#assert(tmp.registers == [20]*8)
#response = client.execute(tmp)
#print (response)

#tmp2 = (tmp & 0X00FF);
#print("read_register... ", tmp2)
#reg_rq=client.write_register(_SLAVE_ID, _ADDR_FETCH_BLOCK_NUM, fetchBlockNum)
'''

'''
fetchBlockNum = 0
reg_rq=client.write_register(_SLAVE_ID, _ADDR_FETCH_BLOCK_NUM, fetchBlockNum)

tmpa = client.read_holding_registers(_SLAVE_ID, _ADDR_BLOCK_INFO, 1)
if not tmpa.isError():
#if isinstance(tmpa, ReadHoldingRegistersResponse):
  chip_block_size = (tmpa.registers[0] & 0X00FF)
  chip_block_num  = (tmpa.registers[0] & 0XFF00)
  print("read_holding_registers... ", tmpa, tmpa.registers, tmpa.registers[0])
  print("CHIP_BLOCK_SIZE: ", chip_block_size)
  print("CHIP_BLOCK_NUM: ", chip_block_num)
else:
  print(f"read_holding_registers error({tmpa})")
  print("error: {}".format(tmpa))
  #pass # handle error condition here
'''

#time.sleep(1)

def doit(arg):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        print ("working on %s" % arg)
        time.sleep(1)
    print("Stopping as you wish.")


def main():
    t = threading.Thread(target=doit, args=("task",))
    t.start()
    time.sleep(5)
    t.do_run = False


if __name__ == "__main__":
    main()


client.close()