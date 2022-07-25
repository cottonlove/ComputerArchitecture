.data

n:
  .align 2
  .word 8

array:
  .align 2
  .word 93,14,23,53,98,10,9,6

newline:
  .asciiz "\n"
space:
  .asciiz " "

.text

# $a0 = n, $a1 = &array[0]
print_array:
  move $t0, $a0
  li $t1, 0
  move $t2, $a1
print_array_loop:
  beq $t1, $t0, print_array_return
  li $v0, 1
  lw $a0, ($t2)
  syscall
  li $v0, 4
  la $a0, space
  syscall
  addi $t1, $t1, 1
  addi $t2, $t2, 4
  j print_array_loop
print_array_return:
  li $v0, 4
  la $a0, newline
  syscall
  jr $ra

################################################################################
# FIXME

# $a0 = n, $a1 = &array[0]
sort_array:
  #$t0 = i(0~)
  li $t0, 0
  addi $t8, $a0, -1
loop1: 
  #j=i+1=$t1
  addi $t1, $t0, 1
loop2:
  # $t2=& array[j], $t3=& array[i]  
  sll $t2, $t1, 2
  sll $t3, $t0, 2
  add $t2, $t2, $a1
  add $t3, $t3, $a1

  #$t4= array[j], $t5= array[i] 
  lw $t4, ($t2)
  lw $t5, ($t3)
  
  #if($t4<$t5) set $t6=1
  slt $t6, $t4, $t5
  beq $t6, $zero, js
  
  #swap
  move $t7, $t5
  sw $t4, ($t3)
  sw $t7, ($t2)
js:
  #j = j+1
  addi $t1, $t1, 1
  bne $t1, $a0, loop2
  #i = i+1
  addi $t0, $t0, 1
  bne $t0, $t8, loop1

  jr $ra

# FIXME
################################################################################

.globl main
main:
  # $s0 = $ra
  move $s0, $ra
  # print_array(n, array)
  lw $a0, n
  la $a1, array
  jal print_array
  # sort_array(n, array)
  lw $a0, n
  la $a1, array
  jal sort_array
  # print_array(n, array)
  lw $a0, n
  la $a1, array
  jal print_array
  # $ra = $s0
  move $ra, $s0
 
  # return
  jr $ra

