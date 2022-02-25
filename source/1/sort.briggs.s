.data
.text
.globl main
_stl_not:
addi $29, $29, -16
sw $ra 0($29)
lw $2, 4($29)
beq $2, $0, _label_1_is_false
lw $2, 0($29)
move $ra, $0
addi $29, $29, 16
jr $2
_label_1_is_false:
lw $2, 0($29)
li $ra, 1
addi $29, $29, 16
jr $2
_stl_logical_and:
addi $29, $29, -16
sw $ra 0($29)
lw $11, 4($29)
lw $10, 8($29)
bne $11, $0, _label_2_second_check
lw $2, 0($29)
move $ra, $0
addi $29, $29, 16
jr $2
_label_2_second_check:
bne $10, $0, _label_3_good_and
lw $2, 0($29)
move $ra, $0
addi $29, $29, 16
jr $2
_label_3_good_and:
lw $2, 0($29)
li $ra, 1
addi $29, $29, 16
jr $2
_stl_logical_or:
addi $29, $29, -16
sw $ra 0($29)
lw $11, 4($29)
lw $10, 8($29)
bne $11, $0, _label_4_success_or
bne $10, $0, _label_4_success_or
lw $2, 0($29)
move $ra, $0
addi $29, $29, 16
jr $2
_label_4_success_or:
lw $2, 0($29)
li $ra, 1
addi $29, $29, 16
jr $2
_stl_pow_int:
addi $29, $29, -24
sw $ra 0($29)
lw $12, 4($29)
lw $11, 8($29)
li $10, 1
bne $12, $0, _label_5_pow_almost_begin
lw $2, 0($29)
move $ra, $0
addi $29, $29, 24
jr $2
_label_5_pow_almost_begin:
bne $11, $0, _label_6_pow_begin
lw $2, 0($29)
li $ra, 1
addi $29, $29, 24
jr $2
_label_6_pow_begin:
_label_7_whileHead:
beq $11, $0, _label_8_whileEnd
li $4, 1
sub $11, $11, $4
mul $10, $10, $12
j _label_7_whileHead
_label_8_whileEnd:
lw $2, 0($29)
move $ra, $10
addi $29, $29, 24
jr $2
_stl_pow_float:
addi $29, $29, -24
sw $ra 0($29)
l.s $f1, 4($29)
li $2, 1
mtc1 $2, $f10
cvt.s.w $f10, $f10
mtc1 $0, $f31
cvt.s.w $f31, $f31
c.eq.s $f1, $f31
bc1f _label_9_pow_almost_begin
lw $2, 0($29)
mtc1 $0, $f0
cvt.s.w $f0, $f0
addi $29, $29, 24
jr $2
_label_9_pow_almost_begin:
lw $2, 8($29)
bne $2, $0, _label_10_pow_begin
lw $2, 0($29)
li $ra, 1
mtc1 $ra, $f0
cvt.s.w $f0, $f0
addi $29, $29, 24
jr $2
_label_10_pow_begin:
_label_11_whileHead:
lw $2, 8($29)
beq $2, $0, _label_12_whileEnd
lw $2, 8($29)
li $4, 1
sub $2, $2, $4
sw $2, 8($29)
mul.s $f10, $f10, $f1
j _label_11_whileHead
_label_12_whileEnd:
lw $2, 0($29)
mov.s $f0, $f10
addi $29, $29, 24
jr $2
main:
addi $29, $29, -200
sw $ra 0($29)
move $11, $0
li $10, 7
move $4, $11
sll $4, $4, 2
add $4, $4, $29
sw $10, 12($4)
li $11, 1
li $10, 2
move $4, $11
sll $4, $4, 2
add $4, $4, $29
sw $10, 12($4)
li $11, 2
li $10, 10
move $4, $11
sll $4, $4, 2
add $4, $4, $29
sw $10, 12($4)
li $11, 3
li $10, 20
move $4, $11
sll $4, $4, 2
add $4, $4, $29
sw $10, 12($4)
li $11, 4
li $10, 5
move $4, $11
sll $4, $4, 2
add $4, $4, $29
sw $10, 12($4)
li $11, 5
li $10, 6
move $4, $11
sll $4, $4, 2
add $4, $4, $29
sw $10, 12($4)
li $11, 6
li $10, 44
move $4, $11
sll $4, $4, 2
add $4, $4, $29
sw $10, 12($4)
li $11, 7
li $10, 33
move $4, $11
sll $4, $4, 2
add $4, $4, $29
sw $10, 12($4)
li $10, 8
move $11, $10
move $12, $0
li $10, 1
sub $18, $11, $10
move $13, $12
_label_13_forHead:
bgt $13, $18, _label_14_forEnd
move $12, $13
li $10, 1
add $14, $13, $10
li $10, 1
sub $17, $11, $10
move $10, $14
_label_15_forHead:
bgt $10, $17, _label_16_forEnd
sll $15, $10, 2
add $15, $15, $29
lw $15, 12($15)
sll $14, $12, 2
add $14, $14, $29
lw $14, 12($14)
li $16, 1
blt $15, $14, _label_17_comparison
move $16, $0
_label_17_comparison:
beq $16, $0, _label_18_if_mid
move $12, $10
j _label_19_if_end
_label_18_if_mid:
_label_19_if_end:
li $4, 1
add $10, $10, $4
j _label_15_forHead
_label_16_forEnd:
sll $10, $13, 2
add $10, $10, $29
lw $10, 12($10)
move $14, $10
sll $15, $12, 2
add $15, $15, $29
lw $15, 12($15)
move $10, $15
move $4, $13
sll $4, $4, 2
add $4, $4, $29
sw $10, 12($4)
move $4, $12
sll $4, $4, 2
add $4, $4, $29
sw $14, 12($4)
li $4, 1
add $13, $13, $4
j _label_13_forHead
_label_14_forEnd:
move $13, $0
li $10, 1
sub $12, $11, $10
move $10, $13
_label_20_forHead:
bgt $10, $12, _label_21_forEnd
sll $11, $10, 2
add $11, $11, $29
lw $11, 12($11)
li $v0, 1
move $a0, $11
syscall
addi $a0, $0, 0xA
addi $v0, $0, 0xB
syscall
li $4, 1
add $10, $10, $4
j _label_20_forHead
_label_21_forEnd:
sw $0, 192($29)
lw $2, 0($29)
lw $ra, 192($29)
addi $29, $29, 200
jr $2
