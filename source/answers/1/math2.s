.data
__a1: .word 0
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
addi $29, $29, -176
sw $ra 0($29)
li $11, 1
li $10, 2
sub $12, $11, $10
li $11, 3
add $10, $12, $11
sw $10, __a1
li $11, 1
li $10, 2
div $12, $11, $10
li $11, 3
mul $10, $12, $11
sw $10, __a1
li $13, 1
li $12, 2
li $10, 3
mul $11, $12, $10
div $10, $13, $11
sw $10, __a1
li $13, 1
li $12, 2
li $10, 3
mul $11, $12, $10
add $10, $13, $11
sw $10, __a1
li $13, 1
li $12, 2
li $10, 3
div $11, $12, $10
sub $10, $13, $11
sw $10, __a1
li $11, 1
li $10, 2
sub $12, $11, $10
li $11, 3
div $10, $12, $11
sw $10, __a1
li $14, 2
li $13, 1
li $12, 2
li $11, 3
sw $12, -20($29)
sw $11, -16($29)
sw $10, 144($29)
sw $11, 140($29)
sw $12, 136($29)
sw $13, 132($29)
sw $14, 128($29)
jal _stl_pow_int
lw $10, 144($29)
lw $11, 140($29)
lw $12, 136($29)
lw $13, 132($29)
lw $14, 128($29)
move $10, $ra
sw $13, -20($29)
sw $10, -16($29)
sw $10, 144($29)
sw $12, 148($29)
sw $13, 132($29)
sw $14, 128($29)
jal _stl_pow_int
lw $10, 144($29)
lw $12, 148($29)
lw $13, 132($29)
lw $14, 128($29)
move $12, $ra
li $10, 2
div $11, $12, $10
add $10, $14, $11
sw $10, __a1
sw $0, 164($29)
lw $2, 0($29)
lw $ra, 164($29)
addi $29, $29, 176
jr $2