# -*- coding: utf-8 -*-

class MIPSRegisters:    
    def __init__(self):            
        return

class MIPS:
    def __init__(self):


        self.MEM_START = 0x80001000
        self.PC = 0x0

        self.special_registers = {
            '$HI': 0x0,
            '$LO': 0x0
        }
        self.registers = {
            # all registers initialized to 0
            '$zero': 0x0,
            '$at' : 0x1,
            '$v0' : 0x2,
            '$v1' : 0x3,
            '$a0' : 0x4,
            '$a1' : 0x5,
            '$a2' : 0x6,
            '$a3' : 0x7,
            '$t0' : 0x8,
            '$t1' : 0x9,
            '$t2' : 0xa,
            '$t3' : 0xb,
            '$t4' : 0xc,
            '$t5' : 0xd,
            '$t6' : 0xe,
            '$t7' : 0xf,
            '$s0' : 0x10,
            '$s1' : 0x11,
            '$s2' : 0x12,
            '$s3' : 0x13,
            '$s4' : 0x14,
            '$s5' : 0x15,
            '$s6' : 0x16,
            '$s7' : 0x17,
            '$t8' : 0x18,
            '$t9' : 0x19,
            '$k0' : 0x1a,
            '$k1' : 0x1b,
            '$gp' : 0x1c,
            '$sp' : 0x1d,
            '$fp' : 0x1e,
            '$ra' :0x1f,   
	    }
        self.register_mem = {
            0x0 : 0,
            0x1 : 0,
            0x2 : 0,
            0x3 : 0,
            0x4 : 0,
            0x5 : 0,
            0x6 : 0,
            0x7 : 0,
            0x8 : 0,
            0x9 : 0,
            0xa : 0,
            0xb : 0,
            0xc : 0,
            0xd : 0,
            0xe : 0,
            0xf : 0,
            0x10 : 0,
            0x11 : 0,
            0x12 : 0,
            0x13 : 0,
            0x14 : 0,
            0x15 : 0,
            0x16 : 0,
            0x17 : 0,
            0x18 : 0,
            0x19 : 0,
            0x1a : 0,
            0x1b : 0,
            0x1c : 0,
            0x1d : 0,
            0x1e : 0,
            0x1f : 0,            
        }

        self.success = "\033[92m[*]\033[97m"
        self.info = "\033[94m[*]\033[97m"

        return
    def inst_parse(self,inst):
        # returns a list for a given instruction name
        # http://www.mrc.uidaho.edu/mrc/people/jff/digital/MIPSir.html
        # https://www.d.umn.edu/~gshute/mips/itype.xhtml
        # https://www.d.umn.edu/~gshute/mips/rtype.xhtml
        # https://www.d.umn.edu/~gshute/mips/jtype.xhtml
        
        # each instruction's 0 index is their type 
        self.inst_table = {
            # r type instruction
            #  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
            # | opcode | rs | rt | rd | shamt | func  |
            # |  6     | 5  |  5 |  5 |   5   |   6   |
            # - - - - - - - - -- - - - - - - - - - - -
            'add'   : ['r','0x00','rs','rt','rd','shamt','0x20'],
            'addu'  : ['r','0x00','rs','rt','rd','shamt','0x21'],
            'sub'   : ['r','0x00','rs','rt','rd','shamt','0x22'],
            'subu'  : ['r','0x00','rs','rt','rd','shamt','0x23'],
            'and'   : ['r','0x00','rs','rt','rd','shamt','0x24'],
            'or'    : ['r','0x00','rs','rt','rd','shamt','0x25'],
            'xor'  :  ['r','0x00','rs','rt','rd','shamt','0x26'],
            'nor'   : ['r','0x00','rs','rt','rd','shamt','0x27'],
            'jr'    : ['r','0x00','rs','rt','rd','shamt','0x08'],
            'slt'   : ['r','0x00','rs','rt','rd','shamt','0x2A'],
            'sltu'  : ['r','0x00','rs','rt','rd','shamt','0x2B'],
            'div'   : ['r','0x00','rs','rt','rd','shamt','0x1A'],
            'divu'  : ['r','0x00','rs','rt','rd','shamt','0x1B'],
            'mfhi'  : ['r','0x00','rs','rt','rd','shamt','0x10'],
            'mflo'  : ['r','0x00','rs','rt','rd','shamt','0x12'],
            
            # i type instruction
            #  _ _ _ _ _ _ _ _ _ _ _ _ _ 
            # | opcode | rs | rt | imm |
            # |  6     | 5  |  5 |  16 | 
            #  - - - - - - - - - - - - - 
            'addi'  : ['i','0x08','rs','rt','imm'],
            'addiu' : ['i','0x09','rs','rt','imm'],
            'andi'  : ['i','0x0C','rs','rt','imm'],
            'beq'   : ['i','0x04','rs','rt','imm'],
            'bne'   : ['i','0x05','rs','rt','imm'],
            'lb'    : ['i','0x20','rs','rt','imm'],
            'lui'   : ['i','0x0F','rs','rt','imm'],
            'lw'    : ['i','0x23','rs','rt','imm'],
            'sw'    : ['i','0x2B','rs','rt','imm'],
            'ori'   : ['i','0x0D','rs','rt','imm'],
            'slti'  : ['i','0x0A','rs','rt','imm'],
            'sltiu' : ['i','0x0B','rs','rt','imm'],
            'sb'    : ['i','0x28','rs','rt','imm'],

            # j type instruction
            #  _ _ _ _ _ _ _ _ _ 
            # | opcode | target |
            # |  6     | 26     | 
            #  - - - - - - - - -  
            'j'     : ['j','0x02', 'addr'],
            'jal'   : ['j','0x03', 'addr'],
        }
        return self.inst_table[inst]

    def check_exception(self, inst_line):
        inst_line = inst_line.split(" ") # ["add","$t0","$s1","10"]
        skeleton = self.inst_parse(inst_line[0])
        if skeleton[0] == 'r':
            if inst_line[0] == 'jr':
                #jr $s
                #0000 00ss sss0 0000 0000 0000 0000 1000
                skeleton[skeleton.index('rd')] = 0x0
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rt')] = 0x0
                skeleton[skeleton.index('shamt')] = "0x0" #shamt val, useless at this point
                return skeleton
            if inst_line[0] == 'div':
                #div $s, $t
                #0000 00ss ssst tttt 0000 0000 0001 1010
                skeleton[skeleton.index('rd')] = 0x0
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[2]])
                skeleton[skeleton.index('shamt')] = "0x0" #shamt val, useless at this point
                return skeleton
            if inst_line[0] == 'divu':
                skeleton[skeleton.index('rd')] = 0x0
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[2]])
                skeleton[skeleton.index('shamt')] = "0x0" #shamt val, useless at this point
                return skeleton
            if inst_line[0] == 'mfhi':
                #mfhi $d
                #0000 0000 0000 0000 dddd d000 0001 0010
                skeleton[skeleton.index('rd')] = hex(self.registers[inst_line[1]])
                return skeleton
            if inst_line[0] == 'mflo':
                #mflo $d
                #0000 0000 0000 0000 dddd d000 0001 0010
                skeleton[skeleton.index('rd')] = hex(self.registers[inst_line[1]])
                return skeleton
            
        if skeleton[0] == 'i':
            if inst_line[0] == 'lb':
                #lb
                #1000 00ss ssst tttt iiii iiii iiii iiii
                # lb $t0 8($s1)
                # ["lb","$t0","8($s1)"]
                skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[2].split("(")[1].replace(")","")])
                skeleton[skeleton.index('imm')] = hex(inst_line[3].split("(")[0])
                return skeleton

            if inst_line[0] == 'lui':
                #lui
                # lui $t, imm
                #0011 11-- ---t tttt iiii iiii iiii iiii
                skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rs')] = ""
                skeleton[skeleton.index('imm')] = hex(int(inst_line[2],16))
                return skeleton          
            
            if inst_line[0] == 'lw':
                #lw
                skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[2].split("(")[1].replace(")","")])
                skeleton[skeleton.index('imm')] = hex(inst_line[3].split("(")[0])
                return skeleton
                
            if inst_line[0] == 'sw':
                # sw
                # sw $t, offset($s)
                # 1010 11ss ssst tttt iiii iiii iiii iiii
                skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[2].split("(")[1].replace(")","")])
                skeleton[skeleton.index('imm')] = hex(inst_line[3].split("(")[0])
                return skeleton

            if inst_line[0] == 'sb':
                # sb
                # sb $t, offset($s)
                # 1010 11ss ssst tttt iiii iiii iiii iiii
                skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[2].split("(")[1].replace(")","")])
                skeleton[skeleton.index('imm')] = hex(inst_line[3].split("(")[0])
                return skeleton

        return False

    def inst_build(self,inst_line):
        # build instruction with only hex values
        _inst = self.check_exception(inst_line)
        if _inst != False:
            return _inst
        inst_line = inst_line.split(" ") # ["add","$t0","$s1","10"]
        skeleton = self.inst_parse(inst_line[0])
        
        if skeleton[0] == 'r':
            skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[2]])
            skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[3]]) # decimal to hex
            skeleton[skeleton.index('rd')] = hex(self.registers[inst_line[1]])
            skeleton[skeleton.index('shamt')] = "0x0" #shamt val, useless at this point

        if skeleton[0] == 'i':
            #addi $t, $s, imm
            #0010 00ss ssst tttt iiii iiii iiii iiii
            skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[2]])
            skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[1]])
            skeleton[skeleton.index('imm')] = hex(int(inst_line[3]))

        if skeleton[0] == 'j':
            skeleton[skeleton.index('addr')] = hex(int(inst_line[1],16))
        return skeleton
    
    
    def assemble(self,inst):
        # converts a full hex instruction to binary
        # note that it won't have type in it after assembledd
        # in other words 1st element will be gone 
        inst_type = inst[0]
        inst =  [self.hex2bin(i) for i in inst[1::]] # ['r', '0x00', '0x0', '0x0', '0xa', '0x0', '0x20']
        if inst_type[0] == 'r':
            inst[0] = inst[0].ljust(6,"0")
            inst[1] = inst[1].ljust(5,"0")
            inst[2] = inst[2].ljust(5,"0")
            inst[3] = inst[3].ljust(5,"0")
            inst[4] = inst[4].ljust(5,"0")
            inst[5] = inst[5].ljust(6,"0")
        if inst_type[0] == 'i':
            inst[0] = inst[0].ljust(6,"0")
            inst[1] = inst[1].ljust(5,"0")
            inst[2] = inst[2].ljust(5,"0")
            inst[3] = inst[3].ljust(16,"0")
        if inst_type[0] == 'j':
            inst[1] = inst[1].ljust(6,"0")
            inst[2] = inst[2].ljust(26,"0")
        return self.bin2hex("".join(i for i in inst))


    def inst_exec(self,inst):
        if inst[0] == 'r':
            # r type instruction
            #  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
            # | opcode | rs | rt | rd | shamt | func  |
            # |  6     | 5  |  5 |  5 |   5   |   6   |
            # - - - - - - - - -- - - - - - - - - - - -
            if inst[-1] == '0x20':
                # ADD
                #Adds two registers and stores the result in a register
                self.register_mem[int(inst[4],16)] = self.register_mem[int(inst[2],16)]  + self.register_mem[int(inst[3],16)]

            if inst[-1] == '0x21':
                # ADDU
                #Adds two registers and stores the result in a register
                self.register_mem[int(inst[4],16)] = self.register_mem[int(inst[2],16)]  + self.register_mem[int(inst[3],16)]

            if inst[-1] == '0x22':
                #SUB
                #Subtracts two registers and stores the result in a register
                self.register_mem[int(inst[4],16)] = self.register_mem[int(inst[2],16)] - self.register_mem[int(inst[3],16)]
            
            if inst[-1] == '0x23':
                #SUBU
                #Subtracts two registers and stores the result in a register
                self.register_mem[int(inst[4],16)] = self.register_mem[int(inst[2],16)] - self.register_mem[int(inst[3],16)]

            if inst[-1] == '0x24':
                #AND
                #Bitwise ands *two registers* and stores the result in a register
                #0000 00ss ssst tttt dddd d000 0010 0100
                self.register_mem[int(inst[4],16)] = self.register_mem[int(inst[2],16)] & self.register_mem[int(inst[3],16)]
                
            if inst[-1] == '0x25':
                #OR
                #Bitwise logical ors two registers and stores the result in a register
                self.register_mem[int(inst[4],16)] = self.register_mem[int(inst[2],16)] | self.register_mem[int(inst[3],16)]

            if inst[-1] == '0x26':
                #XOR
                #Bitwise logical xors two registers and stores the result in a register
                self.register_mem[int(inst[4],16)] = self.register_mem[int(inst[2],16)] ^ self.register_mem[int(inst[3],16)]

            if inst[-1] == '0x27':
                #NOR
                #Bitwise logical nors two registers and stores the result in a register
                self.register_mem[int(inst[4],16)] = ~(self.register_mem[int(inst[2],16)] | self.register_mem[int(inst[3],16)])   

            if inst[-1] == '0x08':
                #JR
                #Jump to the address contained in register $s
                #0000 00ss sss0 0000 0000 0000 0000 1000
                self.register_mem[int(inst[2],16)]
             
            if inst[-1] == '0x2A':
                #SLT
                #If $s is less than $t, $d is set to one. It gets zero otherwise.
                self.register_mem[int(inst[4],16)] = self.register_mem[int(inst[2],16)] if self.register_mem[int(inst[2],16)] < self.register_mem[int(inst[3],16)] else 0x0

            if inst[-1] == '0x2B':
                #SLTU
                #If $s is less than $t, $d is set to one. It gets zero otherwise.
                self.register_mem[int(inst[4],16)] = self.register_mem[int(inst[2],16)] if self.register_mem[int(inst[2],16)] < self.register_mem[int(inst[3],16)] else 0x0

            if inst[-1] == '0x1A':
                #DIV
                #Divides $s by $t and stores the quotient in $LO and the remainder in $HI
                self.special_registers['$LO'] = self.register_mem[int(inst[2],16)] / self.register_mem[int(inst[3],16)]
                self.special_registers['$HI'] = self.register_mem[int(inst[2],16)] % self.register_mem[int(inst[3],16)]
            
            if inst[-1] == '0x1B':
                #DIVU
                #Divides $s by $t and stores the quotient in $LO and the remainder in $HI
                self.special_registers['$LO'] = self.register_mem[int(inst[2],16)] / self.register_mem[int(inst[3],16)]
                self.special_registers['$HI'] = self.register_mem[int(inst[2],16)] % self.register_mem[int(inst[3],16)]
            
            if inst[-1] == '0x10':
                #MFHI
                #The contents of register HI are moved to the specified register.
                #Divides $s by $t and stores the quotient in $LO and the remainder in $HI
                self.register_mem[self.register_mem[int(inst[4],16)]] = self.special_registers['$HI']

            if inst[-1] == '0x12':
                #MFLO
                #The contents of register LO are moved to the specified register
                #mflo $d
                #0000 0000 0000 0000 dddd d000 0001 0010
                self.register_mem[self.register_mem[int(inst[4],16)]] = self.special_registers['$LO']

        if inst[0] == 'i':
            #['i', '0x08', '0x9', '0x8', '0xa']
            # addi $t0 $t1 10
            # $t0 =  0x8,  inst[3] 
            # $t1 =  0x9,  inst[2]
            # 10 =   0xa,  inst[4]
            if inst[1] == '0x08':      
                #Adds a register and a sign-extended immediate value and stores the result in a register
                #addi $t, $s, imm
                #['i', '0x08', '0x9', '0x8', '0xa']
                #0010 00ss ssst tttt iiii iiii iiii iiii
                self.register_mem[int(inst[3],16)] = self.register_mem[int(inst[2],16)] + int(inst[4],16)

            if inst[1] == '0x09':
                #addiu       
                #Adds a register and a sign-extended immediate value and stores the result in a register
                self.register_mem[int(inst[3],16)] = self.register_mem[int(inst[2],16)] + int(inst[4],16)

            if inst[1] == '0x0C':      
                #andi
                #Bitwise ands a register and an immediate value and stores the result in a register
                self.register_mem[int(inst[3],16)] = self.register_mem[int(inst[2],16)]  & int(inst[4],16)

            if inst[1] == '0x04':      
                #beq
                #Branches if the two registers are equal
                #beq $s, $t, offset
                #0001 00ss ssst tttt iiii iiii iiii iiii
                if self.register_mem[int(inst[3],16)] == self.register_mem[int(inst[2],16)]:
                    # jump int(inst[4],16)
                    pass
                else:
                    pass

            if inst[1] == '0x05':   
                #bne
                #Branches if the two registers are not equal
                #bne $s, $t, offset
                #0001 01ss ssst tttt iiii iiii iiii iiii
                if self.register_mem[int(inst[3],16)] != self.register_mem[int(inst[2],16)]:
                    # jump int(inst[4],16)
                    pass
                else:
                    pass
                	
            if inst[1] == '0x20':      
                #lb
                #A byte is loaded into a register from the specified address
                #lb $t, offset($s)
                #1000 00ss ssst tttt iiii iiii iiii iiii
                self.register_mem[int(inst[3],16)] = self.MEM_START + int(inst[2],16) + (4 * int(inst[4],16))
                # (4 * int(inst[4],16)) offset
                # where is located to register int(inst[2],16) + (4 * int(inst[4],16)) 
                # self.MEM + int(inst[2],16) + (4 * int(inst[4],16)) its actualy place in the mem

            if inst[1] == '0x0F':     
                #The immediate value is shifted left 16 bits and stored in the register. The lower 16 bits are zeroes
                # lui $t, imm
                #0011 11-- ---t tttt iiii iiii iiii iiii
                print inst
                self.register_mem[int(inst[3],16)] = int(inst[4],16) << 16
                
            if inst[1] == '0x23':      
                # lw 
                # A word is loaded into a register from the specified address
                # 1000 11ss ssst tttt iiii iiii iiii iiii
                #  
                self.register_mem[int(inst[3],16)] = self.MEM_START + int(inst[2],16) + (4 * int(inst[4],16))

            if inst[1] == '0x2B':      
                #sw
                #The contents of $t is stored at the specified address
                #1010 11ss ssst tttt iiii iiii iiii iiii
                #self.MEM_START + int(inst[2],16) + (4 * int(inst[4],16)) = self.register_mem[int(inst[3],16)] 
                pass

            if inst[1] == '0x0D':      
                #ori
                # ori $t, $s, imm
                self.register_mem[int(inst[3],16)] = self.register_mem[int(inst[2],16)] | int(inst[4],16)
            if inst[1] == '0x0A':      
                #slti
                #If $s is less than immediate, $t is set to one. It gets zero otherwise
                #slti $t, $s, imm
                #0010 10ss ssst tttt iiii iiii iiii iiii
                self.register_mem[int(inst[3],16)] = 1 if  self.register_mem[int(inst[2],16)] < int(inst[4],16) else 0
            if inst[1] == '0x0B':      
                #sltiu 
                self.register_mem[int(inst[3],16)] = 1 if  self.register_mem[int(inst[2],16)] < int(inst[4],16) else 0

            if inst[1] == '0x28':      
                #sb 
                #self.MEM_START + int(inst[2],16) + (4 * int(inst[4],16)) = self.register_mem[int(inst[3],16)] 
                pass
        if inst[0] == 'j':
            if inst[1] == '0x02':
                # j
                # j target
                # PC = nPC; nPC = (PC & 0xf0000000) | (target << 2);
                # Jumps to the calculated address
                print inst
            if inst[1] == '0x03':   
                # jal
                # jumps to the calculated address and stores the return address in $31
                # jal target
                # 0000 11ii iiii iiii iiii iiii iiii iiii
                # $31 = PC + 8 (or nPC + 4); PC = nPC; nPC = (PC & 0xf0000000) | (target << 2);
                print inst
        return 

    def bin2hex(self,val):
        return hex(int(val, 2))
    def hex2bin(self,val):
        return bin(int(val, 16))[2:]

    def info_registers(self):
        print "\n{} Registers".format(self.success)
        for reg, val in sorted(self.registers.items(), key=lambda x: x[1]):
            print "{} : {}".format(reg,hex(self.register_mem[val]))

        print "\n{} Special Registers".format(self.success)
        for reg, val in sorted(self.special_registers.items(), key=lambda x: x[1]):
            print "{} : {}".format(reg,val)
        return