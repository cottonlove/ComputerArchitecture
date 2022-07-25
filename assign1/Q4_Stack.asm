.data

str0:
  .asciiz "TOS_data_size = "
str1:
  .asciiz "TOS_data = "
str2:
  .asciiz "data_size = "
str3:
  .asciiz "data = "
newline:
  .asciiz "\n"
str4:
  .asciiz "num_elements = "

stack_num_elements:
  .align 2
  .word 0

stack_data_size:
  .space 128

stack_data:
  .space 256

.text

# $a0 = TOS_data_size, $a1 = TOS_data
print_TOS:

  addi $sp, $sp, -12
  sw $s0, 0($sp)
  sw $s1, 4($sp)
  sw $s2, 8($sp)

  move $s0, $a0
  move $s1, $a1
  move $s2, $zero
  lb $s2, -1($s0)

  li $v0, 4
  la $a0, str4
  syscall
  li $v0, 1
  lw $a0, stack_num_elements
  syscall
  li $v0, 4
  la $a0, newline
  syscall

  li $v0, 4
  la $a0, str0
  syscall
  li $v0, 1
  move $a0, $s0
  syscall
  li $v0, 4
  la $a0, newline
  syscall

  li $v0, 4
  la $a0, str1
  syscall
  li $v0, 1
  move $a0, $s1
  syscall

  lw $t0, stack_num_elements
  beq $t0, $zero, print_TOS_ret

  li $v0, 4
  la $a0, newline
  syscall

  li $v0, 4
  la $a0, str2
  syscall
  li $v0, 1
  move $a0, $s2
  syscall
  li $v0, 4
  la $a0, newline
  syscall

  li $v0, 4
  la $a0, str3
  syscall

  li $t0, 2
  beq $t0, $s2, print_TOS_2B

  li $t0, 1
  beq $t0, $s2, print_TOS_1B

print_TOS_4B:

  lb $t0, -1($s1)
  sll $t0, $t0, 24

  lb $t1, -2($s1)
  sll $t1, $t1, 24
  srl $t1, $t1, 8
  or $t0, $t0, $t1

  lb $t1, -3($s1)
  sll $t1, $t1, 24
  srl $t1, $t1, 16
  or $t0, $t0, $t1

  lb $t1, -4($s1)
  sll $t1, $t1, 24
  srl $t1, $t1, 24
  or $t0, $t0, $t1

  j print_TOS_ret

print_TOS_2B:

  lb $t0, -1($s1)
  sll $t0, $t0, 8

  lb $t1, -2($s1)
  sll $t1, $t1, 24
  srl $t1, $t1, 24
  or $t0, $t0, $t1

  j print_TOS_ret

print_TOS_1B:

  lb $t0, -1($s1)

print_TOS_ret:

  li $v0, 1
  move $a0, $t0
  syscall

  li $v0, 4
  la $a0, newline
  syscall

  lw $s0, 0($sp)
  lw $s1, 4($sp)
  lw $s2, 8($sp)
  addi $sp, $sp, 12

  jr $ra

################################################################################
# FIXME

# $a0 = TOS_data_size, $a1 = TOS_data,
# $a2 = data_size (1 byte), $a3 = data (up to 4 bytes)
stack_push:

  #space for datasize stack, space for data stack 
  addi $a0, $a0, 1
  add $a1, $a1, $a2

  #push datasize, data to stacks respectively
  sb $a2, -1($a0)
  li $t1, 1
  beq $t1, $a2, push_1b
  li $t1, 2
  beq $t1, $a2, push_2b
  li $t1, 4
  beq $t1, $a2, push_4b
push_1b:
  sb $a3, -1($a1)
  b js  
push_2b:
  #sh $a3, -2($a1)
  sb $a3, -2($a1)
  srl $a3, $a3, 8
  sb $a3, -1($a1)
  b js 

push_4b:
  #sw $a3, -4($a1)
  sb $a3, -4($a1)
  srl $a3, $a3, 8
  sb $a3, -3($a1)
  srl $a3, $a3, 8
  sb $a3, -2($a1)
  srl $a3, $a3, 8
  sb $a3, -1($a1)

js:  
  #stack_num_elements +1
  lw $t3, stack_num_elements
  addi $t3, $t3, 1
  sw $t3, stack_num_elements

  #call print_TOS
  addi $sp, $sp, -8
  sw $a1, 8($sp)
  sw $a0, 4($sp)
  sw $ra, 0($sp)
  jal print_TOS

  lw $ra, 0($sp)
  lw $a0, 4($sp)
  lw $a1, 8($sp)
  addi $sp, $sp, 8
  
  # $v0 = updated_TOS_data_size, $v1 = updated_TOS_data 
  move $v0, $a0
  move $v1, $a1

  jr $ra

##########
# $a0 = TOS_data_size, $a1 = TOS_data
stack_pop:

  #stack_num_elements -1
  lw $t3, stack_num_elements
  addi $t3, $t3, -1
  sw $t3, stack_num_elements

  #pop datasize stack
  lb $t0, -1($a0)
  addi $a0, $a0, -1 
  li $t1, 1
  beq $t1, $t0, pop_1b
  li $t1, 2
  beq $t1, $t0, pop_2b
  li $t1, 4
  beq $t1, $t0, pop_4b

pop_1b:
  #lb $t2, ($a1)
  addi $a1, $a1, -1 
  b jeno
pop_2b:
  #lh $t2, ($a1)
  addi $a1, $a1, -2
  b jeno

pop_4b:
  #lw $t2, ($a1)
  addi $a1, $a1, -4

jeno:

 #call print_TOS
  addi $sp, $sp, -8
  sw $a1, 8($sp)
  sw $a0, 4($sp)
  sw $ra, 0($sp)
  jal print_TOS

  lw $ra, 0($sp)
  lw $a0, 4($sp)
  lw $a1, 8($sp)
  addi $sp, $sp, 8
  
  # $v0 = updated_TOS_data_size, $v1 = updated_TOS_data 
  move $v0, $a0
  move $v1, $a1

  jr $ra

# FIXME
################################################################################

.globl main
main:

  move $s0, $ra

  la $a0, stack_data_size
  la $a1, stack_data
  li $a2, 4
  li $a3, -127
  jal stack_push

  move $a0, $v0
  move $a1, $v1
  li $a2, 1
  li $a3, 4
  jal stack_push

  move $a0, $v0
  move $a1, $v1
  li $a2, 2
  li $a3, -62
  jal stack_push

  move $a0, $v0
  move $a1, $v1
  jal stack_pop

  move $a0, $v0
  move $a1, $v1
  jal stack_pop

  move $a0, $v0
  move $a1, $v1
  jal stack_pop

  # return
  move $ra, $s0
  jr $ra


