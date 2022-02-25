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
addi $29, $29, -16
sw $ra 0($29)
sw $0, 4($29)
lw $2, 0($29)
lw $ra, 4($29)
addi $29, $29, 16
jr $2
