from src.MIPS import *
import os

if __name__ == '__main__':
    mips = MIPS()
    logger = Logger()

    # Set the registers first to see if they are working
    logger.info("""
    Executing: 
    mips.register_mem[mips.registers['$t0']] = 0x32 
    mips.register_mem[mips.registers['$t1']] = 0x10
    mips.register_mem[mips.registers['$t2']] = 0xb
    mips.register_mem[mips.registers['$t3']] = 0xf""")
    
    mips.register_mem[mips.registers['$t0']] = 0x32 
    mips.register_mem[mips.registers['$t1']] = 0x10
    mips.register_mem[mips.registers['$t2']] = 0xb
    mips.register_mem[mips.registers['$t3']] = 0xf
    mips.info_registers()
    input("continue?")
    os.system("clear")


    logger.info("Building instruction 'addi $t0 $t1 10'")
    i = mips.inst_build("addi $t0 $t1 10")
    logger.success(f"Instruction built: {i}")
    mips.inst_exec(i)
    logger.success("Instruction executed")
    mips.info_registers()
    input("continue?")
    os.system("clear")

    
    logger.info("Building instruction 'lui $t0 2'")
    i = mips.inst_build("lui $t0 2")
    logger.success(f"Instruction built: {i}")
    mips.inst_exec(i)
    logger.success("Instruction executed")
    mips.info_registers()
    input("continue?")
    os.system("clear")
    
    
    logger.info("Building instruction 'j 0x8192213'")
    i = mips.inst_build("j 0x8192213")
    logger.success(f"Instruction built: {i}")
    mips.inst_exec(i)
    logger.success("Instruction executed")
    mips.info_registers()

    logger.info("Instruction parse: 'addi'")
    i = mips.inst_parse('addi')
    logger.success(f"Instruction parsed {i}")

    logger.info("Instruction parse: 'add'")
    i = mips.inst_parse('add')
    logger.success(f"Instruction parsed {i}")

    logger.info("Instruction parse: 'xor'")
    i = mips.inst_parse('xor')
    logger.success(f"Instruction parsed {i}")


    # Arithmetics section
    logger.success(f"Hex2bin '0xff': {mips.hex2bin('0xff')}")
    logger.success(f"Hex2bin '0x32': {mips.hex2bin('0x32')}")

    logger.success(f"Bin2hex '10010101': {mips.bin2hex('10010101')}")
    logger.success(f"Bin2hex '110010': {mips.bin2hex('110010')}")


    logger.info("Building instruction 'add $s1 $t0 $s1'")
    i = mips.inst_build("add $s1 $t0 $s1")
    logger.success(f"Instruction built: {i}")
    logger.info(f"Assembling instruction: {i}")
    logger.success(f"Assembled instruction: {mips.inst_assemble(i)}")


    mips.info_registers()
    logger.success(f"Register mem[0x17] : {mips.register_mem[0x17]}")
    logger.success(f"Register $zero: {mips.registers['$zero']}")
    logger.success(f"Register $ra: {mips.registers['$ra']}")



    # R registers test case
    mips.register_mem[mips.registers['$t1']] = 0x10
    mips.register_mem[mips.registers['$t0']] = 0x20 
    mips.register_mem[mips.registers['$t2']] = 0xb
    mips.register_mem[mips.registers['$t3']] = 0xf
    logger.info("""
        Executing : 
        mips.register_mem[mips.registers['$t1']] = 0x10
        mips.register_mem[mips.registers['$t0']] = 0x20 
        mips.register_mem[mips.registers['$t2']] = 0xb
        mips.register_mem[mips.registers['$t3']] = 0xf """)

    mips.inst_exec(mips.inst_build("add $t0 $t0 $t0"))
    mips.info_registers()
    logger.success("Executed: add $t0 $t0 $t0")
    input("continue?")
    os.system("clear")

    mips.inst_exec(mips.inst_build("and $s1 $t2 $t3"))
    mips.info_registers()
    logger.success("Executed: and $s1 $t2 $t3")
    input("continue?")
    os.system("clear")

    mips.inst_exec(mips.inst_build("or $s2 $t0 $t2"))
    mips.info_registers()
    logger.success("Executed: or $s2 $t0 $t2")
    input("continue?")
    os.system("clear")

    mips.inst_exec(mips.inst_build("div $t0 $t1"))
    mips.info_registers()
    logger.success("Executed: div $t0 $t1")
    input("continue?")
    os.system("clear")

    mips.inst_exec(mips.inst_build("slt $t4 $t0 $t1"))
    mips.info_registers()
    logger.success("Executed: slt $t4 $t0 $t1")
    input("continue?")
    os.system("clear")
