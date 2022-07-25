.data

newline:
  .asciiz "\n"

str0:
  .asciiz "Enter a positive integer: "

str1:
  .asciiz "ERROR: received a negative integer!\n"

str2:
  .asciiz "INFO: fibonacci returned "

.text

################################################################################
# FIXME

# $a0: n (<1024)
fibonacci:
  #if(n<0) jmp to label1, set $v0 = 0
  bltz $a0, label1
  #if(n==0 or n==1) jmp to label2, set $v0 =1, $v1 =1
  beq $a0, $zero, label2
  li $t3, 1
  beq $a0, $t3, label2
  #count=n-1, $t0=1, $t1=1
  sub $a0, $a0, $t3
  li $t0, 1
  li $t1, 1
loop:
  add $v1, $t0, $t1
  move $t0, $t1
  move $t1, $v1
  sub $a0, $a0, $t3
  bne $a0, $zero,loop
  b end
  
label1:
  #set $v0 = 0
  move $v0, $zero
b end

label2:
  li $v0, 1
  li $v1, 1
b end

end: 
  jr $ra

# FIXME
################################################################################

.globl main
main:

  # print_string str0
  li $v0, 4
  la $a0, str0
  syscall

  # $t0 = read_int, value of n
  li $v0, 5
  syscall
  move $t0, $v0

  # $s0 = $ra; fibonacci($t0); $ra = $s0
  move $s0, $ra
  move $a0, $t0
  jal fibonacci
  move $ra, $s0

  # $t0 = $v0; $t1 = $v1
  move $t0, $v0
  move $t1, $v1

  # if ($t0 == 0) { goto main_failure }
  beq $t0, $zero, main_failure

main_success:

  # print_string str2
  li $v0, 4
  la $a0, str2
  syscall

  # print_int $t1
  li $v0, 1
  move $a0, $t1
  syscall

  # print_string newline
  li $v0, 4
  la $a0, newline
  syscall

  # goto main_return
  b main_return

main_failure:

  # print_string str1
  li $v0, 4
  la $a0, str1
  syscall

main_return:

  # return
  jr $ra

