import bitarray, bitarray.util
import math

class MiniMIPS:

  def __init__(self, memSize):
    # 32 general-purpose registers
    self.registers = []
    for i in range(32):
      self.registers.append(bitarray.util.zeros(32))
    # byte-addressable memory
    self.memory_size = memSize
    self.memory = bytearray(memSize)

  def setRegister(self, num, data):
    # num: register #, data: 32-bit hex string
    assert (num >= 0 and num < 32)
    self.registers[num] = bitarray.util.hex2ba(data)
    print("[setRegister] registers[{}] = 0x{}".format(num, data))

  def printRegister(self, num):
    # num: register #
    assert (num >= 0 and num < 32)
    data = bitarray.util.ba2hex(self.registers[num])
    print("[printRegister] registers[{}] = 0x{}".format(num, data))

  def setMemory(self, addr, size, data):
    # addr: starting address, size: size in bytes, data: hex string
    assert (size > 0)
    assert (addr >= 0 and addr + size < self.memory_size)
    assert (len(data) == size * 2)
    self.memory[addr : (addr + size)] = bytearray.fromhex(data)
    print("[setMemory] memory[{}:{}] = 0x{}".format(addr, addr + size, data))

  def printMemory(self, addr, size):
    # addr: starting address, size: size in bytes
    assert (size > 0)
    assert (addr >= 0 and addr + size < self.memory_size)
    data = self.memory[addr : (addr + size)].hex()
    print("[printMemory] memory[{}:{}] = 0x{}".format(addr, addr + size, data))

  def execInst(self, inst):
    assert (len(inst) == 8)
    print("[execInst] inst = 0x{}".format(inst))
    # FIXME
    #   You may utilize {set,print}{Register,Memory}() methods when solving the
    #   assignment. 
    #convert hex string to binary string
    res = "{0:032b}".format(int(inst,16))
    strres = str(res)
    #print("resultant string", strres)
    #js = strres[0:6]
    #print("js", js)
    
    #lw instrunction
    if(strres[0:6] == '100011'): 
      #print("js is handsome")
      rs = int(strres[6:11],2) #get source register number in decimal
      rt = int(strres[11:16],2) #get target register number in decimal
      if(rt != 0): #prevent zero register
        #get immediate -> convert it to decimal
        immd = int(strres[16:],2) 
        #hex_immd = hex(immd)

        rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string
        dec_rs_data = int(rs_data, 16) #convert it to decimal
        #hex_rs_data = hex(int(rs_data, 16))#hex_string to hex value

        final_add = immd + dec_rs_data
        #hex_add = hex(final_add)#hex_string
        #print(isinstance(hex_add,str))
        rt_data = self.memory[final_add : (final_add + 4)].hex() #hex_string
        self.registers[rt] = bitarray.util.hex2ba(rt_data)

    #sw instrunction (not tested yet)
    elif(strres[0:6] == '101011'):
      #print("yj loves js")
      rs = int(strres[6:11],2) #get source register number in decimal
      rt = int(strres[11:16],2) #get target register number in decimal
      #if(rt != 0): #prevent zero register
      #get immediate -> convert it to decimal
      immd = int(strres[16:],2) 
      #hex_immd = hex(immd)

      rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string2
      dec_rs_data = int(rs_data, 16) #convert it to decimal
      #hex_rs_data = hex(int(rs_data, 16))#hex_string to hex value

      final_add = immd + dec_rs_data #final memory addres s
      rt_data = bitarray.util.ba2hex(self.registers[rt]) #hex string of rt_data
      #memory[final_add] = rt
      self.memory[final_add : (final_add + 4)] = bytearray.fromhex(rt_data) 

    # addi instruction(not tested yet)
    elif(strres[0:6] == '001000'):
      #print("js lover")
      rs = int(strres[6:11],2) #get source register number in decimal
      rt = int(strres[11:16],2) #get target register number in decimal
      #get immediate -> convert it to decimal
      immd = int(strres[16:],2)
      rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string2
      dec_rs_data = int(rs_data, 16) #convert it to decimal
      final_add = immd + dec_rs_data #$rs + immediate
      hex_add = "{0:08x}".format(final_add)#hex_string
      if(rt != 0): #prevent zero register
        self.registers[rt] = bitarray.util.hex2ba(hex_add)
    # add & sub instruction
    elif(strres[0:6] == '000000'):
      rs = int(strres[6:11],2) #get source register number in decimal
      rt = int(strres[11:16],2) #get target register number in decimal
      rd = int(strres[16:21],2) #get destination register number in decimal
      rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string2
      dec_rs_data = int(rs_data, 16) #convert it to decimal
      rt_data = bitarray.util.ba2hex(self.registers[rt]) #hex_string2
      dec_rt_data = int(rt_data, 16) #convert it to decimal
      # add instruction
      if(strres[26:] == '100000'):
        final_add = dec_rt_data+ dec_rs_data #$rs + $rt
        hex_add = "{0:08x}".format(final_add)
        #hex_add = hex(final_add)#hex_string
        if(rd != 0): #prevent zero register
          self.registers[rd] = bitarray.util.hex2ba(hex_add)
      # sub instruction
      elif(strres[26:] == '100010'):
        final_sub = dec_rs_data - dec_rt_data #$rs - $rt
        hex_sub = "{0:08x}".format(final_sub)#hex_string
        if(rd != 0): #prevent zero register
          self.registers[rd] = bitarray.util.hex2ba(hex_sub)
        
if __name__ == "__main__":
  print("ERROR: 'MiniMIPS.py' should not be invoked directly!")

