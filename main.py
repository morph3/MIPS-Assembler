# -*- coding: utf-8 -*-
from MIPS import MIPS
import argparse
import sys



if __name__ == "__main__":
    
    mips = MIPS()

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="file",help="File name for the assembler")
    parser.add_argument("-i", "--interactive", dest="interactive", help="Interactive mode",action='store_true')
    parser.add_argument("-o", "--output", dest="out_file", help="Output file")
    parser.add_argument("-fmt","--format",dest="format",help="Output format")

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(0)
        
    if args.interactive == True:
        mips.interactive()
    else:
        raw_instr = mips.load_file(args.file) #loads file into memory
        print "{} Raw instructions".format(mips.success)
        for inst in raw_instr:
            print "Instruction: {}".format(inst)
            _hex,_bin = mips.inst_assemble(mips.inst_build(inst))
            print "Hex: {}\nBin: {}".format(_hex,_bin)
        mips.info_memory()
        mips.exec_memory()
        mips.info_registers()
    
    if args.out_file != None:
        fw = open(args.out_file,"w")
        for inst in raw_instr:
            _hex,_bin = mips.inst_assemble(mips.inst_build(inst))
            if args.format == 'hex':
                fw.write("{}\n".format(_hex))
            else:
                fw.write("{}\n".format(_bin))
        fw.close
        #print "Hex: {}\nBin: {}".format(i_hex, i_bin)



    """
    mips.register_mem[mips.registers['$t0']] = 0x32 
    mips.register_mem[mips.registers['$t1']] = 0x10
    mips.register_mem[mips.registers['$t2']] = 0xb
    mips.register_mem[mips.registers['$t3']] = 0xf
    mips.info_registers()
    raw_input("continue?")

    mips.inst_exec(mips.inst_build("addi $t0 $t1 10"))
    mips.info_registers()
    raw_input("continue?")

    mips.inst_exec(mips.inst_build("lui $t0 2"))
    mips.info_registers()
    raw_input("continue?")

    mips.inst_exec(mips.inst_build("j 0x8192213"))
    mips.info_registers()
    raw_input
    """


    """
    - Test Cases - 
    print mips.inst_parse('addi')
    print mips.inst_parse('add') # ['r', '0x00', 'rs', 'rt', 'rd', 'shamt', '0x20']    
    print mips.inst_parse('xor')

    print mips.hex2bin('0xff')
    print mips.hex2bin('0x32')
    print mips.bin2hex('10010101')
    print mips.bin2hex('110010')

    print mips.inst_build("add $s1 $t0 10") # ['r', '0x00', '0x0', '0xa', '0x0', 0, '0x20']
    print mips.assemble(i)


    mips.info_registers()
    print mips.register_mem[0x17]

    print mips.registers['$zero']
    print mips.registers['$ra']    


    R registers test case
    mips.register_mem[mips.registers['$t1']] = 0x10
    mips.register_mem[mips.registers['$t0']] = 0x20 
    mips.register_mem[mips.registers['$t2']] = 0xb
    mips.register_mem[mips.registers['$t3']] = 0xf


    mips.inst_exec(mips.inst_build("add $t0 $t0 $t0"))
    mips.info_registers()
    raw_input("continue?")

    mips.inst_exec(mips.inst_build("and $s1 $t2 $t3"))
    mips.info_registers()
    raw_input("continue?")

    mips.inst_exec(mips.inst_build("or $s2 $t0 $t2"))
    mips.info_registers()
    raw_input("continue?")

    mips.inst_exec(mips.inst_build("div $t0 $t1"))
    mips.info_registers()
    raw_input("continue?")

    mips.inst_exec(mips.inst_build("slt $t4 $t0 $t1"))
    mips.info_registers()
    raw_input("continue?")
    """