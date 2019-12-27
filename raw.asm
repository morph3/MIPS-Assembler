sort: 
    addi $sp, $sp, -20 # make room on stack for 5 registers
    sw $ra, 16($sp)# save $ra on stack
    sw $s3, 12($sp) # save $s3 on stack
    sw $s2, 8($sp)# save $s2 on stack
    sw $s1, 4($sp)# save $s1 on stack
    sw $s0, 0($sp)# save $s0 on stack
    addi $s1, $s0, -1#j=i–1
    for2tst:
        slti $t0, $s1, 0 #reg$t0=1if$s1<0(j<0)
        bne $t0, $zero, exit2# go to exit2 if $s1 < 0 (j < 0)
        sll $t1, $s1, 2# reg $t1=j*4
        add $t2, $s2, $t1# reg $t2 = v + (j * 4)
        lw $t3, 0($t2)# reg $t3 = v[j]
        lw $t4, 4($t2)# reg $t4 = v[j + 1]
        slt $t0, $t4, $t3 # reg $t0 = 0 if $t4 Š $t3
        beq $t0, $zero, exit2# go to exit2 if $t4 Š $t3
exit2: 
    addi $s0, $s0, 1 # i += 1
    j for2tst # jump to test of outer loop
