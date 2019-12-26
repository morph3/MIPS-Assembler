# -*- coding: utf-8 -*-

"""

Saving Registers
sort: 
    addi $sp,$sp, –20 # make room on stack for 5 registers
    sw $ra, 16($sp)# save $ra on stack
    sw $s3,12($sp) # save $s3 on stack
    sw $s2, 8($sp)# save $s2 on stack
    sw $s1, 4($sp)# save $s1 on stack
    sw $s0, 0($sp)# save $s0 on stack

Procedure body 
Move parameters 
    move $s2, $a0 # copy parameter $a0 into $s2 (save $a0)
    move $s3, $a1 # copy parameter $a1 into $s3 (save $a1)

Outer loop
    move $s0, $zero# i = 0
    for1tst:slt $t0, $s0,$s3 #reg$t0=0if$s0Š$s3(iŠn)
    beq $t0, $zero, exit1# go to exit1 if $s0 Š $s3 (i Š n)

Inner loop
    addi $s1, $s0, –1#j=i–1
    for2tst:slti $t0, $s1,0 #reg$t0=1if$s1<0(j<0)
    bne $t0, $zero, exit2# go to exit2 if $s1 < 0 (j < 0)
    sll $t1, $s1, 2# reg $t1=j*4
    add $t2, $s2, $t1# reg $t2 = v + (j * 4)
    lw $t3, 0($t2)# reg $t3 = v[j]
    lw $t4, 4($t2)# reg $t4 = v[j + 1]
    slt $t0, $t4, $t3 # reg $t0 = 0 if $t4 Š $t3
    beq $t0, $zero, exit2# go to exit2 if $t4 Š $t3

Pass parameters and call
    move $a0, $s2 # 1st parameter of swap is v (old $a0)
    move $a1, $s1 # 2nd parameter of swap is j
    jal swap # swap code shown in Figure 2.25
Inner loop 
    addi $s1, $s1, –1# j –= 1
    j for2tst # jump to test of inner loop

Outer loop 
    exit2: 
        addi $s0, $s0, 1 # i += 1
        j for1tst # jump to test of outer loop
Restoring registers
exit1: 
    lw $s0, 0($sp) # restore $s0 from stack
    lw $s1, 4($sp)# restore $s1 from stack
    lw $s2, 8($sp)# restore $s2 from stack
    lw $s3,12($sp) # restore $s3 from stack
    lw $ra,16($sp) # restore $ra from stack
    addi $sp,$sp, 20 # restore stack pointer
Procedure return
    jr $ra # return to calling routine

"""


from MIPS import MIPS

if __name__ == "__main__":
    
    
    #TODO: build a working logic with mem
    #      inst_exec works fine almost %90
    #TODO: PC
    #TODO: functions and labels

    mips = MIPS()
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
