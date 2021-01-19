# -*- coding: utf-8 -*-
import sys
class Logger:
    def __init__(self):
        self.green = "\033[92m[*]\033[97m"
        self.blue = "\033[94m[*]\033[97m"
        self.reset = "\033[0;0m"
    def success(self,msg):
        sys.stdout.write(f"{self.green}{msg}\n")
    def info(self,msg):
        sys.stdout.write(f"{self.blue}{msg}\n")
    def out(self,msg):
        sys.stdout.write(f"{msg}\n")

class MIPS:

    def __init__(self):
        self.logger = Logger()
        self.twos_complement = lambda x, count=8: "".join(map(lambda y:str((x>>y)&1), range(count-1, -1, -1)) )

        self.MEM_START = 0x80001000
        self.MEM = {}
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


        return

    def check_exception(self, inst_line):
        inst_line = inst_line.split(" ") # ["add","$t0","$s1","10"]
        skeleton = self.inst_parse(inst_line[0])
        if skeleton[0] == 'r':
            if inst_line[0] == 'jr':
                #jr $s
                #0000 00ss sss0 0000 0000 0000 0000 1000
                skeleton[skeleton.index('rd')] = "0x0"
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rt')] = "0x0"
                skeleton[skeleton.index('shamt')] = "0x0" #shamt val, useless at this point
                return skeleton
            if inst_line[0] == 'div':
                #div $s, $t
                #0000 00ss ssst tttt 0000 0000 0001 1010
                skeleton[skeleton.index('rd')] = "0x0"
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[2]])
                skeleton[skeleton.index('shamt')] = "0x0" #shamt val, useless at this point
                return skeleton
            if inst_line[0] == 'divu':
                skeleton[skeleton.index('rd')] = "0x0"
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[2]])
                skeleton[skeleton.index('shamt')] = "0x0" #shamt val, useless at this point
                return skeleton
            if inst_line[0] == 'mfhi':
                #mfhi $d
                #0000 0000 0000 0000 dddd d000 0001 0010
                skeleton[skeleton.index('rd')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rs')] = "0x0"
                skeleton[skeleton.index('rt')] = "0x0"
                skeleton[skeleton.index('shamt')] = "0x0"
                return skeleton
            if inst_line[0] == 'mflo':
                #mflo $d
                #0000 0000 0000 0000 dddd d000 0001 0010
                skeleton[skeleton.index('rd')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rs')] = "0x0"
                skeleton[skeleton.index('rt')] = "0x0"
                skeleton[skeleton.index('shamt')] = "0x0"
                return skeleton
            if inst_line[0] == 'sll':
                #sll $d, $t, h
                #0000 0000 0000 0000 dddd d000 0001 0010
                #0000 00ss ssst tttt dddd dhhh hh00 0000
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[2]])
                skeleton[skeleton.index('rt')] = "0x0"
                skeleton[skeleton.index('rd')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('shamt')] = hex(int(inst_line[3]))
                return skeleton
            

        if skeleton[0] == 'i':
            if inst_line[0] == 'lb':
                #lb
                #1000 00ss ssst tttt iiii iiii iiii iiii
                # lb $t0 8($s1)
                # ["lb","$t0","8($s1)"]
                skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[2].split("(")[1].replace(")","")])
                skeleton[skeleton.index('imm')] = hex(int(inst_line[2].split("(")[0]))
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
                skeleton[skeleton.index('imm')] = hex(int(inst_line[2].split("(")[0]))
                return skeleton
                
            if inst_line[0] == 'sw':
                # sw
                # sw $t, offset($s)
                # 1010 11ss ssst tttt iiii iiii iiii iiii
                skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[2].split("(")[1].replace(")","")])
                skeleton[skeleton.index('imm')] = hex(int(inst_line[2].split("(")[0]))
                return skeleton

            if inst_line[0] == 'sb':
                # sb
                # sb $t, offset($s)
                # 1010 11ss ssst tttt iiii iiii iiii iiii
                skeleton[skeleton.index('rt')] = hex(self.registers[inst_line[1]])
                skeleton[skeleton.index('rs')] = hex(self.registers[inst_line[2].split("(")[1].replace(")","")])
                skeleton[skeleton.index('imm')] = hex(int(inst_line[2].split("(")[0]))
                return skeleton

        return False
    
    def inst_parse(self,inst):
        # returns a list for a given instruction name
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
            'sll'  : ['r','0x00','rs','rt','rd','shamt','0x0'],

            
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
            skeleton[skeleton.index('rs')] = hex(int(self.registers[inst_line[2]]))
            skeleton[skeleton.index('rt')] = hex(int(self.registers[inst_line[1]]))
            if 'x' in inst_line[3]:
                skeleton[skeleton.index('imm')] = inst_line[3]
            else:
                skeleton[skeleton.index('imm')] = hex(int(inst_line[3]))

        if skeleton[0] == 'j':
            skeleton[skeleton.index('addr')] = (inst_line[1])
        return skeleton   
    
    def inst_assemble(self,inst):
        # converts a full hex instruction to binary and hex value and returns them
        inst_type = inst[0]
        _tmp = inst
        inst =  [self.hex2bin(i) for i in inst[1::]] # ['r', '0x00', '0x0', '0x0', '0xa', '0x0', '0x20']
        if inst_type[0] == 'r':
            inst[0] = inst[0].rjust(6,"0")
            inst[1] = inst[1].rjust(5,"0")
            inst[2] = inst[2].rjust(5,"0")
            inst[3] = inst[3].rjust(5,"0")
            inst[4] = inst[4].rjust(5,"0")
            inst[5] = inst[5].rjust(6,"0")

        if inst_type[0] == 'i':
            inst[0] = inst[0].rjust(6,"0")
            inst[1] = inst[1].rjust(5,"0")
            inst[2] = inst[2].rjust(5,"0")
            if '-' in _tmp[-1]:
                _tmp[-1] = -1 * int(_tmp[-1].replace('-0x',''),16)
                inst[3] = self.twos_complement(_tmp[-1],16).rjust(16,"0")
            else:
                inst[3] = inst[3].rjust(16,"0")

        if inst_type[0] == 'j':
            inst[0] = inst[0].rjust(6,"0")
            inst[1] = inst[1].rjust(26,"0")
            #self.twos_complement(int(inst[1])).rjust(26,"0")

        _hex = self.bin2hex("".join(i for i in inst))
        _bin = "".join(i for i in inst)
        return _hex, _bin

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
                self.register_mem[int(inst[4],16)] = 0x1 if self.register_mem[int(inst[2],16)] < self.register_mem[int(inst[3],16)] else 0x0

            if inst[-1] == '0x2B':
                #SLTU
                #If $s is less than $t, $d is set to one. It gets zero otherwise.
                self.register_mem[int(inst[4],16)] = 0x1 if self.register_mem[int(inst[2],16)] < self.register_mem[int(inst[3],16)] else 0x0

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

            if inst[-1] == '0x0':
                #SLL
                #Shifts a register value left by the shift amount listed in the instruction and places the result in a third register. Zeroes are shifted in
               
                self.register_mem[int(inst[4],16)] = self.register_mem[int(inst[2],16)] << self.register_mem[int(inst[5],16)]
            


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
                    self.PC == inst[3]
                else:
                    self.PC == "0x0"

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
                self.PC = inst[2]


            if inst[1] == '0x03':   
                # jal
                # jumps to the calculated address and stores the return address in $31
                # jal target
                # 0000 11ii iiii iiii iiii iiii iiii iiii
                # $31 = PC + 8 (or nPC + 4); PC = nPC; nPC = (PC & 0xf0000000) | (target << 2);
                self.PC = inst[2]

        return 

    def bin2hex(self,val):
        return hex(int(val, 2))
    
    def hex2bin(self,val):
        return bin(int(val, 16))[2:]
       
    def interactive(self):

        self.logger.info("There is no memory in this mode")
        self.logger.info("Enter q to exit interactive mode")
        self.logger.info("Enter r to see the register information")
        cmd = input("~#: ").strip()
        while(cmd != 'q'):
            if cmd == 'r':
                self.info_registers()
                cmd = input("~#: ").strip()
                continue
            try:
                i = self.inst_build(cmd)
                _backup_i = i.copy() #copy it
                #self.logger.success(f"Instruction build {i}")
                _hex, _bin = self.inst_assemble(i)
                self.logger.success(f"Instruction assembled\nHex value: {_hex}\nBinary value: {_bin}")
                self.inst_exec(_backup_i)
                self.logger.success("Executed the instruction")

            except KeyError:
                self.logger.info("You have probably entered a wrong instruction, please check your instruction")
            except ValueError:
                self.logger.info("You have something wrong with your syntax")
            except TypeError:
                self.logger.info("You have something wrong with your syntax")

            cmd = input("~#: ").strip()
            
        return 

    def load_file(self,file_name):
        #loads file to memory and returns list of instruction
        f = open(file_name, "r")
        #['sort: \n', '    addi $sp,$sp, -20 # make room on stack for 5 registers\n', '    sw $ra, 16($sp)# save $ra on stack\n', '    sw $s3,12($sp) # save $s3 on stack\n', '    sw $s2, 8($sp)# save $s2 on stack\n', '    sw $s1, 4($sp)# save $s1 on stack\n', '    sw $s0, 0($sp)# save $s0 on stack\n', '\n']   
        raw_instr = []
    
        #load file into memory
        self.MEM[self.MEM_START] = 0x0 
        _mem_counter = 0x0
        for line in f:
            _line = line.split("#")[0].replace("\n",'').replace("    ","").replace(',','')
            self.MEM[self.MEM_START+_mem_counter] = _line
            _mem_counter += 0x4

        # replace addresses with labels    
        for outer_addr, outer_inst in self.MEM.items():
            if ':' in outer_inst:
                for inner_addr, inner_inst in self.MEM.items():
                    self.MEM[inner_addr] = self.MEM[inner_addr].replace(outer_inst.split(':')[0],str(hex(outer_addr)))

        for outer_addr, outer_inst in self.MEM.items():
            if ':' not in outer_inst:
                raw_instr.append(outer_inst)

        self.info_memory()
        f.close()

        return raw_instr

    def info_memory(self):
        
        self.logger.success("Memory")
        for address, val in sorted(self.MEM.items(), key=lambda x: x[0]):
            self.logger.out(f"{hex(address)} : {val}")
        return

    def info_registers(self):
        self.logger.success("Registers")
        for reg, val in sorted(self.registers.items(), key=lambda x: x[1]):
            self.logger.out(f"{reg} : {hex(self.register_mem[val])}")

        self.logger.success("Special Registers")
        for reg, val in sorted(self.special_registers.items(), key=lambda x: x[1]):
            self.logger.out(f"{reg} : {val}")

        return

    def exec_memory(self):
        self.PC = self.MEM_START            
        for address, inst in self.MEM.items():
            self.PC = address
            if ':' in inst:
                continue
            else:
                self.inst_exec(self.inst_build(inst))
        return
