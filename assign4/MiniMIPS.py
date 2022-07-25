import bitarray, bitarray.util

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
    
    self.ncycle = 0

    #IF/ID latch(8bit hex string) 0. Inst 1.(PC + 4)
    self.IF_ID = [None for x in range(0,5)]

    #ID/EX latch(8bit hex string) 0. instruction string 1. (PC + 4) 2.rs value
      #//lw,sw:  3. rd index 4. Immd(16bit->signed extended) 
      #//R: 3. rd index 4. rt 
      #//beq: 3. rt 4. Immd(16bit->signed extended)
    self.ID_EX = [None for x in range(0,5)]

    #EX/MEM latch(8bit hex string) 0. instruction string 1. (PC + 4) 
      #//lw, sw: 2.rs + immd  3. rd index
      #//R: 2.operation result  3. rd index
      #//beq: 2.(rs==rt) 3. immd  
    self.EX_MEM = [None for x in range(0,5)]

    #MEM/WB latch(8bit hex string) 0. instruction string
    #//lw, sw: 1.data 2. rd index (sw: do nothing so just 'pass')
    #//R: 1. operation result 2. rd index
    #//beq: 1. operation result 2. rd index(do nothing so just 'pass')
    self.MEM_WB = [None for x in range(0,5)]
    
    #self.js = 0


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

  def twos_complement(self, n, w): #n: number, w:num of bits
    if n & (1 << (w-1)): n = n - (1 << w)
    return n

  def Fetch(self):
    #print("Fetch")
    #print("Fetch: ", self.js)
    
    #load instruction in instMemory pointed by pc value
    pc_data = bitarray.util.ba2hex(self.pc) #hexstring
    d_pc = int(pc_data, 16) #convert hex string to decimal int
    #print(d_pc)########
    #instruction
    inst = self.inst_memory[d_pc : (d_pc+ 4)].hex()
    #print(inst)
    #convert hex string to binary string
    res = "{0:032b}".format(int(inst,16))
    #store instruction(32bit string) in latch
    self.IF_ID[0] = res #.append(res)

    #update pc value(add 4)
    d_pc = d_pc + 4
    h_pc = "{0:08x}".format(d_pc)#hex_string
    self.pc = bitarray.util.hex2ba(h_pc)
    #store pc+4 (8bit hex string) in latch
    self.IF_ID[1] = h_pc #.append(h_pc)

  def Decode(self):
    if not self.IF_ID: #list is empty
      #print("IF_ID is empty") #############3
      pass
    else:
      #print("IF_ID is not empty") ##########
      # load 32bit instruction
      strres = self.IF_ID[0]
      #print(strres)
      #lw
      if(strres[0:6] == '100011'): 
      
        self.ID_EX[0] = "lw" #.append("lw")
        self.ID_EX[1] = self.IF_ID[1] #.append(self.IF_ID[1]) # still store pc+4

        #print("js is handsome")
        rs = int(strres[6:11],2) #get source register number in decimal
        rt = int(strres[11:16],2) #get target register number in decimal
        rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string
        dec_rs_data = int(rs_data, 16) #convert it to decima
        ##if(rd != 0): #prevent zero register

        self.ID_EX[2] = dec_rs_data #.append(dec_rs_data) #rs data in decimal
        self.ID_EX[3] = rt #.append(rt) #index of rd in decimal

        #get immediate -> convert it to decimal
        immd = int(strres[16:],2) 

        self.ID_EX[4] = immd #.append(immd) #immd in decimal

        #hex_immd = hex(immd)

      #sw
      elif(strres[0:6] == '101011'):
        self.ID_EX[0] = "sw" #.append("sw")
        self.ID_EX[1] = self.IF_ID[1] #.append(self.IF_ID[1]) # still store pc+4
        #print("yj loves js")

        rs = int(strres[6:11],2) #get source register number in decimal
        rt = int(strres[11:16],2) #get target register number in decimal
        rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string
        dec_rs_data = int(rs_data, 16) #convert it to decima
        self.ID_EX[2] = dec_rs_data #.append(dec_rs_data) #rs data in decimal
        self.ID_EX[3] = rt #.append(rt) #index of rd in decimal
        #if(rt != 0): #prevent zero register
        #get immediate -> convert it to decimal
        immd = int(strres[16:],2) 
        self.ID_EX[4]=immd #.append(immd) #immd in decimal
        #hex_immd = hex(immd)

      #add & sub & and & or & slt
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
          self.ID_EX[0] = "add" #.append("add")
          self.ID_EX[1]= self.IF_ID[1] #.append(self.IF_ID[1]) # still store pc+4
          self.ID_EX[2]= twos_rs #.append(twos_rs) #store signed decimal of rs
          self.ID_EX[3]= twos_rt #.append(twos_rt) #store signed decimal of rt
          self.ID_EX[4]= rd #.append(rd) #store index of rd

        # sub instruction(not tested yet)
        elif(strres[26:] == '100010'):
          self.ID_EX[0]= "sub" #.append("sub")
          self.ID_EX[1]= self.IF_ID[1] #.append(self.IF_ID[1]) # still store pc+4
          self.ID_EX[2]= twos_rs #.append(twos_rs) #store signed decimal of rs
          self.ID_EX[3]= twos_rt #.append(twos_rt) #store signed decimal of rt
          self.ID_EX[4]= rd #.append(rd) #store index of rd
        
        #logical and(not tested yet)
        elif(strres[26:] == '100100'): 
          self.ID_EX[0] = "and" #.append("and")
          self.ID_EX[1] = self.IF_ID[1] #.append(self.IF_ID[1]) # still store pc+4

          rs = int(strres[6:11],2) #get source register number in decimal
          rt = int(strres[11:16],2) #get target register number in decimal
          rd = int(strres[16:21],2) #get destination register number in decimal
          rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string2
          #convert hex string to bitarray
          rs_bstring = bitarray.util.hex2ba(rs_data) #hex string to bitarray
          rt_bstring = bitarray.util.hex2ba(rt_data) #hex string to bitarray
          self.ID_EX[2] = rs_bstring #.append(rs_bstring) #store 32bit string stored in rs
          self.ID_EX[3] = rt_bstring #.append(rt_bstring) #store 32bit string stored in rt
          self.ID_EX[4] = rd #.append(rd) #store index of rd

        #logical or(not tested yet)
        elif(strres[26:] == '100101'): 
          self.ID_EX[0] = "or" #.append("or")
          self.ID_EX[1] = self.IF_ID[1] #.append(self.IF_ID[1]) # still store pc+4

          rs = int(strres[6:11],2) #get source register number in decimal
          rt = int(strres[11:16],2) #get target register number in decimal
          rd = int(strres[16:21],2) #get destination register number in decimal
          rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string2
          #convert hex string to bitarray
          rs_bstring = bitarray.util.hex2ba(rs_data) #hex string to bitarray
          rt_bstring = bitarray.util.hex2ba(rt_data) #hex string to bitarray
          
          self.ID_EX[2] = rs_bstring #.append(rs_bstring) #store 32bit string stored in rs
          self.ID_EX[3] = rt_bstring #.append(rt_bstring) #store 32bit string stored in rt
          self.ID_EX[4] = rd #.append(rd) #store index of rd

        #set-on-less-than(slt. signed)(not tested yet)
        elif(strres[26:] == '101010'): 
          self.ID_EX[0] = "slt" #.append("slt")
          self.ID_EX[1] = self.IF_ID[1] #.append(self.IF_ID[1]) # still store pc+4

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
          self.ID_EX[2] = twos_rs #.append(twos_rs) #store signed decimal of rs
          self.ID_EX[3] = twos_rt #.append(twos_rt) #store signed decimal of rt
          self.ID_EX[4] = rd #.append(rd) #store index of rd

      #beq
      if(strres[0:6] == '000100'):
        self.ID_EX[0] = "beq" #.append("beq")
        self.ID_EX[1] = self.IF_ID[1] #.append(self.IF_ID[1]) # still store pc+4

        rs = int(strres[6:11],2) #get source register number in decimal
        rt = int(strres[11:16],2) #get target register number in decimal
        rs_data = bitarray.util.ba2hex(self.registers[rs]) #hex_string2
        dec_rs_data = int(rs_data, 16) #convert it to decimal

        rt_data = bitarray.util.ba2hex(self.registers[rt]) #hex_string2
        dec_rt_data = int(rt_data, 16) #convert it to decimal
        immd = int(strres[16:],2) #get target address number in decimal
        self.ID_EX[2]= dec_rs_data #.append(dec_rs_data) #store decimal of rs
        self.ID_EX[3]= dec_rt_data #.append(dec_rt_data) #store decimal of rt
        self.ID_EX[4]= immd #.append(immd) #store decimal of immd
        
      #print("Decode: ", self.js+1)

  def Exec(self):
    if not self.ID_EX: #list is empty
      #print("IF_ID is empty")
      pass
    else:
      #print(self.ID_EX[0])
      #print("IF_ID is not empty")
      if(self.ID_EX[0] == "lw"):
        #print("lwexe") #####################
        self.EX_MEM[0] = self.ID_EX[0] #.append(self.ID_EX[0]) #"lw"
        self.EX_MEM[1] = self.ID_EX[1] #.append(self.ID_EX[1]) # still store pc+4
        temp = self.ID_EX[2] + self.ID_EX[4] #rs_data + immd
        self.EX_MEM[2] = temp #.append(temp)
        self.EX_MEM[3] = self.ID_EX[3] #.append(self.ID_EX[3]) #still store rd index

      elif(self.ID_EX[0] == "sw"):
        self.EX_MEM[0] = self.ID_EX[0] #.append(self.ID_EX[0]) #"sw"
        self.EX_MEM[1]= self.ID_EX[1] #.append(self.ID_EX[1]) # still store pc+4
        temp = self.ID_EX[2] + self.ID_EX[4] #rs_data + immd
        self.EX_MEM[2]= temp #.append(temp)
        self.EX_MEM[3]= self.ID_EX[3] #.append(self.ID_EX[3]) #still store rd index

      elif(self.ID_EX[0] == "add"):
        self.EX_MEM[0]= self.ID_EX[0] #.append(self.ID_EX[0]) #"add"
        self.EX_MEM[1]= self.ID_EX[1] #.append(self.ID_EX[1]) # still store pc+4

        final_add = self.ID_EX[2] + self.ID_EX[3] #twos_rs + twos_rd
        if(final_add < 0):
          hex_add = '{0:08x}'.format(final_add & (2**32-1))
        else:
          hex_add = "{0:08x}".format(final_add)#hex_string

        self.EX_MEM[2]= hex_add #.append(hex_add)

        self.EX_MEM[3]= self.ID_EX[4] #.append(self.ID_EX[4]) #still store rd index

      elif(self.ID_EX[0] == "sub"):
        self.EX_MEM[0]= self.ID_EX[0] #.append(self.ID_EX[0]) #"sub"
        self.EX_MEM[1]= self.ID_EX[1] #.append(self.ID_EX[1]) # still store pc+4

        final_sub = self.ID_EX[2] - self.ID_EX[3] #twos_rs - twos_rd
        if(final_sub < 0):
          hex_sub = '{0:08x}'.format(final_sub & (2**32-1))
        else:
          hex_sub = "{0:08x}".format(final_sub)#hex_string
        self.EX_MEM[2] = hex_sub #.append(hex_sub)

        self.EX_MEM[3]= self.ID_EX[4] #.append(self.ID_EX[4]) #still store rd index 

      elif(self.ID_EX[0] == "and"):
        self.EX_MEM[0]= self.ID_EX[0] #.append(self.ID_EX[0]) #"and"
        self.EX_MEM[1]= self.ID_EX[1] #.append(self.ID_EX[1]) # still store pc+4

        temp = self.ID_EX[2] & self.ID_EX[3] #twos_rs & twos_rd
        rd_hstring = bitarray.util.ba2hex(temp) #bitarray to hex string
        self.EX_MEM[2]= rd_hstring #.append(rd_hstring)

        self.EX_MEM[3]=self.ID_EX[4] #.append(self.ID_EX[4]) #still store rd index

      elif(self.ID_EX[0] == "or"):
        self.EX_MEM[0]= self.ID_EX[0] #.append(self.ID_EX[0]) #"or"
        self.EX_MEM[1]= self.ID_EX[1] #.append(self.ID_EX[1]) # still store pc+4

        temp = self.ID_EX[2] | self.ID_EX[3] #twos_rs | twos_rd
        rd_hstring = bitarray.util.ba2hex(temp) #bitarray to hex string
        self.EX_MEM[2] = rd_hstring #.append(rd_hstring)

        self.EX_MEM[3] = self.ID_EX[4] #.append(self.ID_EX[4]) #still store rd index

      elif(self.ID_EX[0] == "slt"):
        self.EX_MEM[0]=self.ID_EX[0] #.append(self.ID_EX[0]) #"slt"
        self.EX_MEM[1]= self.ID_EX[1] #.append(self.ID_EX[1]) # still store pc+4
        if(self.ID_EX[2] < self.ID_EX[3]):
          self.EX_MEM[2]= True #.append(True)
        else:
          self.EX_MEM[2]= False #.append(False)
        self.EX_MEM[3]= self.ID_EX[4] #.append(self.ID_EX[4]) #still store rd index

      elif(self.ID_EX[0] == "beq"):
        self.EX_MEM[0]=self.ID_EX[0] #.append(self.ID_EX[0]) #"beq"
        self.EX_MEM[1]= self.ID_EX[1] #.append(self.ID_EX[1]) # still store pc+4
        if(self.ID_EX[2] == self.ID_EX[3]):
          self.EX_MEM[2]= True #.append(True)
        else:
          self.EX_MEM[2]= False #.append(False)
        self.EX_MEM[3]= self.ID_EX[4] #.append(self.ID_EX[4]) #still store immd

      #print("Exec: ", self.js+2)
  
  def Mem(self):
    if not self.EX_MEM: #list is empty
      pass
    else:

      if(self.EX_MEM[0] == "lw"):
        #print("lwMem")
        self.MEM_WB[0]=self.EX_MEM[0] #.append(self.EX_MEM[0]) #"lw"
        self.MEM_WB[1]= self.EX_MEM[1] #.append(self.EX_MEM[1]) # still store pc+4

        final_add =  self.EX_MEM[2] #access memory address
        #get rt_data from data memory
        rt_data = self.data_memory[final_add : (final_add + 4)].hex()  #hex_string
        

        self.MEM_WB[2] = rt_data #.append(rt_data)
        self.MEM_WB[3] = self.EX_MEM[3] #.append(self.EX_MEM[3]) #still store rd index

      elif(self.EX_MEM[0] == "sw"):
        self.MEM_WB[0]= self.EX_MEM[0] #.append(self.EX_MEM[0]) #"sw"
        self.MEM_WB[1]= self.EX_MEM[1] #.append(self.EX_MEM[1]) # still store pc+4

        rt_data = bitarray.util.ba2hex(self.registers[self.EX_MEM[3]]) #hex string of rt_data
        final_add =  self.EX_MEM[2] #access memory address
        #memory[final_add] = rt
        #store. memory access
        self.data_memory[final_add : (final_add + 4)] = bytearray.fromhex(rt_data)

      elif(self.EX_MEM[0] == "add"): #do nothing
        self.MEM_WB[0]=self.EX_MEM[0] #.append(self.EX_MEM[0]) #"add"
        self.MEM_WB[1]=self.EX_MEM[1] #.append(self.EX_MEM[1]) # still store pc+4
        self.MEM_WB[2]=self.EX_MEM[2] #.append(self.EX_MEM[2]) # still store alu result
        self.MEM_WB[3]=self.EX_MEM[3] #.append(self.EX_MEM[3]) # still store rd index
        

      elif(self.EX_MEM[0] == "sub"): #do nothing
        self.MEM_WB[0]=self.EX_MEM[0] #.append(self.EX_MEM[0]) #"sub"
        self.MEM_WB[1]=self.EX_MEM[1] #.append(self.EX_MEM[1]) # still store pc+4
        self.MEM_WB[2]=self.EX_MEM[2] #.append(self.EX_MEM[2]) # still store alu result
        self.MEM_WB[3]=self.EX_MEM[3] #.append(self.EX_MEM[3]) # still store rd index
        
        '''self.MEM_WB.append(self.EX_MEM[0]) #"sub"
        self.MEM_WB.append(self.EX_MEM[1]) # still store pc+4
        self.MEM_WB.append(self.EX_MEM[2]) # still store alu result
        self.MEM_WB.append(self.EX_MEM[3]) # still store rd index'''

      elif(self.EX_MEM[0] == "and"): #do nothing
        self.MEM_WB[0]=self.EX_MEM[0] #.append(self.EX_MEM[0]) #"and"
        self.MEM_WB[1]=self.EX_MEM[1] #.append(self.EX_MEM[1]) # still store pc+4
        self.MEM_WB[2]=self.EX_MEM[2] #.append(self.EX_MEM[2]) # still store alu result
        self.MEM_WB[3]=self.EX_MEM[3] #.append(self.EX_MEM[3]) # still store rd index

        '''self.MEM_WB.append(self.EX_MEM[0]) #"and"
        self.MEM_WB.append(self.EX_MEM[1]) # still store pc+4
        self.MEM_WB.append(self.EX_MEM[2]) # still store alu result
        self.MEM_WB.append(self.EX_MEM[3]) # still store rd index'''

      elif(self.EX_MEM[0] == "or"): #do nothing
        self.MEM_WB[0]=self.EX_MEM[0] #.append(self.EX_MEM[0]) #"or"
        self.MEM_WB[1]=self.EX_MEM[1] #.append(self.EX_MEM[1]) # still store pc+4
        self.MEM_WB[2]=self.EX_MEM[2] #.append(self.EX_MEM[2]) # still store alu result
        self.MEM_WB[3]=self.EX_MEM[3] #.append(self.EX_MEM[3]) # still store rd index

        '''self.MEM_WB.append(self.EX_MEM[0]) #"or"
        self.MEM_WB.append(self.EX_MEM[1]) # still store pc+4
        self.MEM_WB.append(self.EX_MEM[2]) # still store alu result
        self.MEM_WB.append(self.EX_MEM[3]) # still store rd index'''

      elif(self.EX_MEM[0] == "slt"): #do nothing
        self.MEM_WB[0]=self.EX_MEM[0] #.append(self.EX_MEM[0]) #"add"
        self.MEM_WB[1]=self.EX_MEM[1] #.append(self.EX_MEM[1]) # still store pc+4
        self.MEM_WB[2]=self.EX_MEM[2] #.append(self.EX_MEM[2]) # still store true/false
        self.MEM_WB[3]=self.EX_MEM[3] #.append(self.EX_MEM[3]) # still store rd index
        '''self.MEM_WB.append(self.EX_MEM[0]) #"slt"
        self.MEM_WB.append(self.EX_MEM[1]) # still store pc+4
        self.MEM_WB.append(self.EX_MEM[2]) # still store true/false
        self.MEM_WB.append(self.EX_MEM[3]) # still store rd index'''

      elif(self.EX_MEM[0] == "beq"): #if true: pc value update to (pc+4) + (4*immd)
        self.MEM_WB[0]= self.EX_MEM[0] #.append(self.EX_MEM[0]) #"beq"
        #update pc_value
        if(self.EX_MEM[2] == True):
          #self.EX_MEM[1]: hex string
          jeno = int(self.EX_MEM[1], 16)
          #print(jeno)
          #print(self.EX_MEM[3])
          d_pc = (jeno) + (self.EX_MEM[3]*4) - 4 #in fetch, always add 4 so sub 4 in advance
          h_pc = "{0:08x}".format(d_pc)#hex_string
          self.pc = bitarray.util.hex2ba(h_pc)
        else: ##################
          pass
      #print("Mem:", self.js+3)
  
  def WB(self):
    if not self.MEM_WB: #list is empty
      pass

    else:
      if(self.MEM_WB[0] == "lw"):
        #print("lw")
        if(self.MEM_WB[3]!=0):
          self.registers[self.MEM_WB[3]] = bitarray.util.hex2ba(self.MEM_WB[2])
        else:
          pass
      elif(self.MEM_WB[0] == "sw"): #do nothing
        pass

      elif(self.MEM_WB[0] == "add"): 
        #print("adding")
        if(self.MEM_WB[3]!=0):
          self.registers[self.MEM_WB[3]] = bitarray.util.hex2ba(self.MEM_WB[2])
        else:
          pass
      elif(self.MEM_WB[0] == "sub"):  
        if(self.MEM_WB[3]!=0):
          self.registers[self.MEM_WB[3]] = bitarray.util.hex2ba(self.MEM_WB[2])
        else:
          pass
      elif(self.MEM_WB[0] == "and"): 
        if(self.MEM_WB[3]!=0):
          self.registers[self.MEM_WB[3]] = bitarray.util.hex2ba(self.MEM_WB[2])
        else:
          pass
      elif(self.MEM_WB[0] == "or"): 
        if(self.MEM_WB[3]!=0):
          self.registers[self.MEM_WB[3]] = bitarray.util.hex2ba(self.MEM_WB[2])
        else:
          pass
      elif(self.MEM_WB[0] == "slt"): 
        if(self.MEM_WB[3]!=0):
          if(self.MEM_WB[2] == True):
            self.registers[self.MEM_WB[3]] = bitarray.util.hex2ba('00000001')
          else:
            self.registers[self.MEM_WB[3]] = bitarray.util.hex2ba('00000000')
        else:
          pass
      
      elif(self.MEM_WB[0] == "beq"): #do nothing
        pass
      
      #print("Mem:", self.js+3)

    #print("WB:", self.js+4)

  def advanceCycle(self):
    # FIXME
    print("[advanceCycle] $pc = 0x{}".format(bitarray.util.ba2hex(self.pc)))
    self.ncycle = self.ncycle + 1
    #cycle = [ self.Fetch,  self.Decode, self.Exec, self.Mem, self.WB]

    if (self.ncycle == 1):
      self.Fetch()
    elif (self.ncycle == 2):
      self.Decode()
      self.Fetch()
    elif (self.ncycle == 3):
      self.Exec()
      self.Decode()
      self.Fetch()
    elif (self.ncycle == 4):
      self.Mem()
      self.Exec()
      self.Decode()
      self.Fetch()
    elif (self.ncycle == 5):
      self.WB()
      self.Mem()
      self.Exec()
      self.Decode()
      self.Fetch()
    elif (self.ncycle >= 6):
      #print("ncycle >= 6")
      
      self.WB()
      self.Mem()
      self.Exec()
      self.Decode()
      self.Fetch()
    '''self.Fetch()
    self.Decode()
    self.Exec()
    self.Mem()
    self.WB()'''
    #self.js = self.js + 1

    pass

if __name__ == "__main__":
  print("ERROR: 'MiniMIPS.py' should not be invoked directly!")

