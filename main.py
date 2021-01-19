# -*- coding: utf-8 -*-
from src.MIPS import *
import argparse
import sys



if __name__ == "__main__":
    
    mips = MIPS()
    logger = Logger()
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="file",help="File name for the assembler")
    parser.add_argument("-i", "--interactive", dest="interactive", help="Interactive mode",action='store_true')
    parser.add_argument("-o", "--output", dest="out_file", help="Output file")
    parser.add_argument("-fmt","--format",dest="format",help="Output format")

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit()
        
    if args.interactive:
        mips.interactive()
    else:
        raw_instr = mips.load_file(args.file) #loads file into memory
        logger.success("Raw instructions")
        for inst in raw_instr:
            logger.success(inst)
            _hex,_bin = mips.inst_assemble(mips.inst_build(inst))
            logger.out(f"Hex: {_hex}\nBin: {_bin}")

        mips.info_memory()
        #mips.exec_memory()
        #mips.info_registers()
    
    if args.out_file != None:
        fw = open(args.out_file,"w")
        for inst in raw_instr:
            _hex,_bin = mips.inst_assemble(mips.inst_build(inst))
            if args.format == 'hex':
                fw.write(f"{_hex}\n")
            else:
                fw.write(f"{_bin}\n")
        fw.close()


