This program will compute the nth fibonacci number
Date: 12/5/22
The output is stored in R1
Anything typed here is ignored!

.text
MOVI R0 0 //comments are also supported
MOVI R1 1
MOVI R2 0

MOVI R3 5

SUBI R3 R3 2

//I love commenting ;)
Loop: 
CBZ R3 End

MOV R2 R0
MOV R0 R1
MOV R1 R2

ADD R1 R1 R0

SUBI R3 R3 1
B Loop

End: STOP

//also note that .data can actually come before the .text segment and the assembler will run fine
.data
0x1123 0xffff
0x6623 0x4487
