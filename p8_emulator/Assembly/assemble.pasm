# fibbonacci

# incrementer and max
LDI reg1 1
LDI reg2 0
LDI reg3 5

# fibbonacci starters
LDI reg4 0
LDI reg5 1
LDI reg6 0

# loop
ADD reg2 reg1 reg2

ADD reg6 reg4 reg5
MOV reg4 reg5
MOV reg5 reg6

CMP reg2 reg3
JMP JNZ 13
HLT