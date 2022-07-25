import bitarray, bitarray.util

#assn3
class MiniMIPS:

  def __init__(self, dataMemSize, instMemSize):
    # 32 general-purpose registers ($0 ~ $31)
    self.registers = []
    for i in range(32):
      self.registers.append(bitarray.util.zeros(32))
    # byte-addressable data memory
    self.data_memory_size = dataMemSize
    self.data_memory = bytearray(self.data_memory_size)
    # byte-addressable instruction memory
    self.inst_memory_size = instMemSize
    self.inst_memory = bytearray(self.inst_memory_size)
    # $pc
    self.pc = bitarray.util.zeros(32)

  def setRegister(self, num, data):
    # num: register #, data: 32-bit hex string
    assert (num >= 0 and num < 32)
    self.registers[num] = bitarray.util.hex2ba(data)

  def printRegister(self, num):
    # num: register #
    assert (num >= 0 and num < 32)
    data = bitarray.util.ba2hex(self.registers[num])
    print("[printRegister] ${} = 0x{}".format(num, data))

  def printPC(self):
    print("[printPC] $pc = 0x{}".format(bitarray.util.ba2hex(self.pc)))

  def setDataMemory(self, addr, size, data):
    # addr: starting address, size: size in bytes, data: hex string
    assert (size > 0)
    assert (addr >= 0 and addr + size < self.data_memory_size)
    assert (len(data) == size * 2)
    self.data_memory[addr : (addr + size)] = bytearray.fromhex(data)

  def setInstMemory(self, addr, size, data):
    # addr: starting address, size: size in bytes, data: hex string
    assert (size > 0)
    assert (addr >= 0 and addr + size < self.inst_memory_size)
    assert (len(data) == size * 2)
    self.inst_memory[addr : (addr + size)] = bytearray.fromhex(data)

  def printDataMemory(self, addr, size):
    # addr: starting address, size: size in bytes
    assert (size > 0)
    assert (addr >= 0 and addr + size < self.data_memory_size)
    data = self.data_memory[addr : (addr + size)].hex()
    print("[printDataMemory] data_memory[{}:{}] = 0x{}".format(addr, addr + size, data))

  def printInstMemory(self, addr, size):
    # addr: starting address, size: size in bytes
    assert (size > 0)
    assert (addr >= 0 and addr + size < self.inst_memory_size)
    data = self.inst_memory[addr : (addr + size)].hex()
    print("[printInstMemory] inst_memory[{}:{}] = 0x{}".format(addr, addr + size, data))

  ##
  ##def twosCom_binDec(self, bin, digit): #bin to decimal #bin: binary string, digit: length 
    ##while len(bin)<digit :
        ##bin = '0'+bin
    ##if bin[0] == '0':
      ##return int(bin, 2)
    ##else:
      ##return -1 * (int(''.join('1' if x == '0' else '0' for x in bin), 2) + 1)

  ##def twosCom_decBin(self,dec, digit): #decimal to bin #dec: decimal int
    ##if dec>=0:
      ##bin1 = bin(dec).split("0b")[1]
      ##while len(bin1)<digit :
        ##bin1 = '0'+bin1
      ##return bin1
    ##else:
      ##bin1 = -1*dec
      ##return bin(dec-pow(2,digit)).split("0b")[1]

  ##def hex2(self, n): #n: minus decimal int  to 8 bit hex string
    ##return "0x%s"%("00000000%s"%(hex(n&0xffffffff)[2:-1]))[-8:]

  def twos_complement(self, n, w): #n: number, w:num of bits
    if n & (1 << (w-1)): n = n - (1 << w)
    return n

  def advanceCycle(self):
    # FIXME
    print("[advanceCycle] $pc = 0x{}".format(bitarray.util.ba2hex(self.pc)))
    #load instruction in instMemory pointed by pc value
    pc_data = data = bitarray.util.ba2hex(self.pc) #hexstring
    d_pc = int(pc_data, 16) #convert hex string to decimal int
    #print(pc_data)
    #instruction
    inst = self.inst_memory[d_pc : (d_pc+ 4)].hex()
    #print(inst)
    #convert hex string to binary string
    res = "{0:032b}".format(int(inst,16))
    #print(type(res))
    strres = str(res)
    
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
        rt_data = self.data_memory[final_add : (final_add + 4)].hex()  #hex_string
        self.registers[rt] = bitarray.util.hex2ba(rt_data)
      #update pc value(add 4)
      d_pc = d_pc + 4
      h_pc = "{0:08x}".format(d_pc)#hex_string
      self.pc = bitarray.util.hex2ba(h_pc)

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
      self.data_memory[final_add : (final_add + 4)] = bytearray.fromhex(rt_data) 
      #update pc value(add 4)
      d_pc = d_pc + 4
      h_pc = "{0:08x}".format(d_pc)#hex_string
      self.pc = bitarray.util.hex2ba(h_pc)

################################################# sw, lw

    # addi instruction(not tested yet)
    elif(strres[0:6] == '001000'):
      #print("js lover")
      rs = int(strres[6:11],2) #get source register number in decimal
      rt = int(strres[11:16],2) #get target register number in decimal
      #get immediate -> convert it to decimal
      immd = int(strres[16:],2)
      #print("bin", bin(immd))
      ##print("immd:", immd) 

      rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string2
      dec_rs_data = int(rs_data, 16) #convert it to decimal
      ##print("dec_rs_data:", dec_rs_data)
      twos_rs = self.twos_complement(dec_rs_data, 32) #interpret the value of reg as 2's complement
      ##print("twos_rs:", twos_rs) #
      twos_immd = self.twos_complement(immd, 16) #interpret the value of reg as 2's complement
      ##print("twos_immd:", twos_immd) #

      final_add = twos_immd + twos_rs #$rs + immediate
      ##print("final_add:", final_add) #

      if(final_add < 0):
        hex_add = '{0:08x}'.format(final_add & (2**32-1))
      else:
        hex_add = "{0:08x}".format(final_add)#hex_string
      if(rt != 0): #prevent zero register
        self.registers[rt] = bitarray.util.hex2ba(hex_add)
      #update pc value(add 4)
      d_pc = d_pc + 4
      h_pc = "{0:08x}".format(d_pc)#hex_string
      self.pc = bitarray.util.hex2ba(h_pc)

    # add & sub instruction // logical and/or // set-on-less-than(slt)->signed
    elif(strres[0:6] == '000000'):
      rs = int(strres[6:11],2) #get source register number in decimal
      rt = int(strres[11:16],2) #get target register number in decimal
      rd = int(strres[16:21],2) #get destination register number in decimal
      rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string2
      dec_rs_data = int(rs_data, 16) #convert it to decimal
      #print("dec_rs_data",dec_rs_data)
      twos_rs = self.twos_complement(dec_rs_data, 32) #interpret the value of reg as 2's complement
      #print("twos_rs", twos_rs)
      rt_data = bitarray.util.ba2hex(self.registers[rt]) #hex_string2
      dec_rt_data = int(rt_data, 16) #convert it to decimal
      ##print("dec_rs_data",dec_rt_data)
      twos_rt = self.twos_complement(dec_rt_data, 32) #interpret the value of reg as 2's complement
      ##print("twos_rs", twos_rt)

      # add instruction
      if(strres[26:] == '100000'):
        final_add = twos_rs + twos_rt #$rs + $rt
        if(final_add < 0):
          hex_add = '{0:08x}'.format(final_add & (2**32-1))
          ##hex_add = self.hex2(final_add)#hex_string
          ##print(final_add)
          #print(hex_add)
          #ff_add = self.twosCom_decBin(final_add, 32)
          #print(ff_add)
          #hex_add = "{0:08x}".format(ff_add)
        else:
          hex_add = "{0:08x}".format(final_add)#hex_string

        ##hex_add = "{0:08x}".format(final_add)
        ##print(hex_add) ##
        #hex_add = hex(final_add)#hex_string
        if(rd != 0): #prevent zero register
          self.registers[rd] = bitarray.util.hex2ba(hex_add)
        #update pc value(add 4)
        d_pc = d_pc + 4
        h_pc = "{0:08x}".format(d_pc)#hex_string
        self.pc = bitarray.util.hex2ba(h_pc)

      # sub instruction(not tested yet)
      elif(strres[26:] == '100010'):
        final_sub = twos_rs - twos_rt #$rs - $rt
        if(final_sub<0):
          hex_sub = '{0:08x}'.format(final_sub & (2**32-1))
        else:
          hex_sub = "{0:08x}".format(final_sub)#hex_string
        if(rd != 0): #prevent zero register
          self.registers[rd] = bitarray.util.hex2ba(hex_sub)  
        #update pc value(add 4)
        d_pc = d_pc + 4
        h_pc = "{0:08x}".format(d_pc)#hex_string
        self.pc = bitarray.util.hex2ba(h_pc)

############################################# add, sub, addi
  
      #logical and(not tested yet)
      elif(strres[26:] == '100100'): 
        rs = int(strres[6:11],2) #get source register number in decimal
        rt = int(strres[11:16],2) #get target register number in decimal
        rd = int(strres[16:21],2) #get destination register number in decimal
        rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string2
        #convert hex string to bitarray
        rs_bstring = bitarray.util.hex2ba(rs_data) #hex string to bitarray
        rt_bstring = bitarray.util.hex2ba(rt_data) #hex string to bitarray
        rd_bstring = rs_bstring & rt_bstring #bit-by-bit and operation

        rd_hstring = bitarray.util.ba2hex(rd_bstring) #bitarray to hex string
        if(rd != 0): #prevent zero register
          self.registers[rd] = bitarray.util.hex2ba(rd_hstring)
        #update pc value(add 4)
        d_pc = d_pc + 4
        h_pc = "{0:08x}".format(d_pc)#hex_string
        self.pc = bitarray.util.hex2ba(h_pc)

      #logical or(not tested yet)
      elif(strres[26:] == '100101'): 
        rs = int(strres[6:11],2) #get source register number in decimal
        rt = int(strres[11:16],2) #get target register number in decimal
        rd = int(strres[16:21],2) #get destination register number in decimal
        rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string2
        #convert hex string to bitarray
        rs_bstring = bitarray.util.hex2ba(rs_data) #hex string to bitarray
        rt_bstring = bitarray.util.hex2ba(rt_data) #hex string to bitarray
        rd_bstring = rs_bstring | rt_bstring #bit-by-bit or operation

        rd_hstring = bitarray.util.ba2hex(rd_bstring) #bitarray to hex string
        if(rd != 0): #prevent zero register
          self.registers[rd] = bitarray.util.hex2ba(rd_hstring)     
        #update pc value(add 4)
        d_pc = d_pc + 4
        h_pc = "{0:08x}".format(d_pc)#hex_string
        self.pc = bitarray.util.hex2ba(h_pc)

############################logical and, or


      #set-on-less-than(slt. signed)(not tested yet)
      elif(strres[26:] == '101010'): 
        rs = int(strres[6:11],2) #get source register number in decimal
        rt = int(strres[11:16],2) #get target register number in decimal
        rd = int(strres[16:21],2) #get destination register number in decimal
        rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string2
        dec_rs_data = int(rs_data, 16) #convert it to decimal
        twos_rs = self.twos_complement(dec_rs_data, 32) #interpret the value of reg as 2's complement
        #print(twos_rs) #20042874
       
        rt_data = bitarray.util.ba2hex(self.registers[rt]) #hex_string2
        dec_rt_data = int(rt_data, 16) #convert it to decimal
        twos_rt = self.twos_complement(dec_rt_data, 32) #interpret the value of reg as 2's complement
        #print(twos_rt) #65535

        if(rd != 0): #prevent zero register
          if(twos_rs < twos_rt):
            self.registers[rd] = bitarray.util.hex2ba('00000001') 
          else:
            self.registers[rd] = bitarray.util.hex2ba('00000000')

        #update pc value(add 4)
        d_pc = d_pc + 4
        h_pc = "{0:08x}".format(d_pc)#hex_string
        self.pc = bitarray.util.hex2ba(h_pc) 

############################ slt

    #conditional jump(branch on equal)(beq)
    if(strres[0:6] == '000100'):
      rs = int(strres[6:11],2) #get source register number in decimal
      rt = int(strres[11:16],2) #get target register number in decimal
      rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string2
      dec_rs_data = int(rs_data, 16) #convert it to decimal

      rt_data = bitarray.util.ba2hex(self.registers[rt]) #hex_string2
      dec_rt_data = int(rt_data, 16) #convert it to decimal
      immd = int(strres[16:],2) #get target address number in decimal
      if(dec_rs_data == dec_rt_data):
        #update pc value(add 4)
        d_pc = (d_pc + 4) + (immd*4)
        h_pc = "{0:08x}".format(d_pc)#hex_string
        self.pc = bitarray.util.hex2ba(h_pc)
      else:
        #update pc value(add 4)
        d_pc = d_pc + 4
        h_pc = "{0:08x}".format(d_pc)#hex_string
        self.pc = bitarray.util.hex2ba(h_pc)

    #unconditional jump (j) (not tested yet)
    #first 4 bit of pc + immd(26bit) + '00' -> 32bit
    if(strres[0:6] == '000010'):
      #get pc binary value
      b_pc = self.pc #bitarray
      s_pc = b_pc.to01() #bitarray to string of 0s, 1s
      #print(type(b_pc))
      #print(s_pc)
      bit4_pc = s_pc[0:4]
      #print(bit4_pc)
      b_immd = strres[6:]
      up_b_pc = bit4_pc + b_immd + '00'
      #print(up_b_pc)
      #update pc value(add 4)
      #d_pc = (immd*4)
      d_pc = int(up_b_pc, 2)
      h_pc = "{0:08x}".format(d_pc)#hex_string
      self.pc = bitarray.util.hex2ba(h_pc)   

    #print("[advanceCycle] $pc = 0x{}".format(bitarray.util.ba2hex(self.pc)))
    pass

if __name__ == "__main__":
  print("ERROR: 'MiniMIPS.py' should not be invoked directly!")

