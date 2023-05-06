## CPU and Instruction Architecture

My CPU design uses a 16 bit architecture as it consists of 16 general purpose registers which each can
store up to 16 bits. The instruction and data memory have been allocated in 16 bit chunks.
It can perform the four fundamental operations which are addition, subtraction, multiplication, and
division with and without immediate values.
Load and store as well as branching are also supported!

### Instruction Set Architecture

Each instruction is 16 bits in length
Registers must be referenced with the prefix R which go from R0 ... R15
Registers are 4 bits each because that is the minimum number of bits required to register ids 0 to 15
Please note that all immediate values are treated as signed and this applies to all instructions

### Arithmatic Instructions

Rd, Rm Rn | imm are all 4 bits each
- ADD Rd Rm Rn (Opcode: 0001)
- ADDI Rd Rm imm (Opcode: 0010)
- SUB Rd Rm Rn (Opcode: 0011)
- SUBI Rd Rm imm (Opcode: 0100)
- MUL Rd Rm Rn (Opcode: 0101)
- MULI Rd Rm imm (Opcode: 0110)
- DIV Rd Rm Rn (Opcode: 0111)
- DIVI Rd Rm imm (Opcode: 1000)

### Move and Memory Related Instructions

Rd and Rm are 4 bits each which leaves 4 zeros at the end of the MOV instruction
- MOV Rd Rm (Opcode: 1001)
Rd is 4 bits and the immediate value is 8 bits (since that is the remaining space to use)
- MOVI Rd imm (Opcode: 1010)
Rd, Rm, and imm are 4 bits
- Ldr (1011 Rd, Rm, imm)
- Str (1100, Rd, Rm, imm)

### Branching Instructions

The label/offset is 12 bits
- B label (Opcode: 1101)
Rm is 4 bits and the label/offset is 8 bits
- Cbz (1110 Rm, label) → Branch when Rm = 0
- Cbgz (1111 Rm, label) → Branch when Rm > 0

This is a special instruction which must come at the end of the text segment which indicates that
the instructions are completed
It consists of a full 16 bit zeroed instruction
- Stop (All 16 bits are 0s)

### Example Assembly Programs
This program will compute the nth fibonacci number!
```assembly
.text
MOVI R0 0 //comments are also supported
MOVI R1 1
MOVI R2 0

MOVI R3 5

SUBI R3 R3 2

Loop: 
CBZ R3 End

MOV R2 R0
MOV R0 R1
MOV R1 R2

ADD R1 R1 R0

SUBI R3 R3 1
B Loop

End: STOP


.data
0x1123 0xffff
0x6623 0x4487
```
