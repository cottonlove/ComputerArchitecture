.data

array:
  .align 2
  .space 128

newline:
  .asciiz "\n"
space:
  .asciiz " "
str0:
  .asciiz "n =? "
str1:
  .asciiz "idx0 =? "
str2:
  .asciiz "idx1 =? "

.text

# $a0 = n
print_array:
  move $t0, $a0
  li $t1, 0
  la $t2, array
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

# $a0 = n, fill the array form 0 to n-1
populate_array:
  li $t0, 0
  la $t1, array
  li $t2, 1
  li $t3, 4
populate_array_loop:
  #fill array
  sw $t0, 0($t1)
  #$t0+1, $t1+4
  add $t0, $t0, $t2
  add $t1, $t1, $t3
  bne $t0, $a0, populate_array_loop   
  jr $ra

# $a0 = idx0, $a1 = idx1
reverse_array:
  #$t0 = &array[0]
  la $t0, array

  # $t1 = i(0~)
  li $t1, 0

  #$t9: for mul 
  #li $t9, 4

  #$t2 = ((idx1-idx0)//2)
  sub $t2, $a1, $a0
  sra $t2, $t2, 1

  #&array[indx0] = t3
  sll $t3, $a0, 2
  add $t3, $t3, $t0
 
  #&array[indx1-1] = t4
  addi $t4, $a1, -1
  sll $t4, $t4, 2
  add $t4, $t4, $t0

reverse_array_loop:
  # $t5=4*i
  sll $t5, $t1, 2

  #&array[indx0+i]=$t6
  add $t6, $t3, $t5
  #&array[(indx1-1)-i]=$t7
  sub $t7, $t4, $t5
  
  #array[indx0+i]=$t8=temp
  lw $t8, ($t6)
  #array[(indx1-1)-i]=$t7
  lw $t9, ($t7)
  # array[idx0 + i] = array[(idx1 - 1) - i]
  sw $t9, ($t6)
  #&array[(indx1-1)-i]=$t7
  #sub $t7, $t4, $t5
  #array[(idx1 - 1) - i] = tmp
  sw $t8, ($t7)

  addi $t1, $t1, 1
  bne $t1, $t2, reverse_array_loop

  jr $ra

# FIXME
################################################################################

.globl main
main:
  # print_string str0
  li $v0, 4
  la $a0, str0
  syscall
  # $s0 = read_int
  li $v0, 5
  syscall
  move $s0, $v0

  # print_string str1
  li $v0, 4
  la $a0, str1
  syscall
  # $s1 = read_int
  li $v0, 5
  syscall
  move $s1, $v0

  # print_string str2
  li $v0, 4
  la $a0, str2
  syscall
  # $s2 = read_int
  li $v0, 5
  syscall
  move $s2, $v0

  # $s0 = n, $s1 = idx0, $s2 = idx1

  # $s3 = $ra
  move $s3, $ra
  # populate_array($s0)
  move $a0, $s0
  jal populate_array
  # print_array($s0)
  move $a0, $s0
  jal print_array
  # reverse_array($s1, $s2)
  move $a0, $s1
  move $a1, $s2
  jal reverse_array
  # print_array($s0)
  move $a0, $s0
  jal print_array
  # $ra = $s3
  move $ra, $s3

  # return
  jr $ra

