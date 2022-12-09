from instruction import Instruction
from utils import Utils

class ArithmaticInstruction(Instruction):
    def __init__(self, opcode: str):
        super().__init__(opcode)

    def encode(self, tokens: list[str]) -> str:
        output = ""

        output += hex(int(self.opcode, 2))[2:]

        for i in range(len(tokens)):
            if (tokens[i].startswith("R")):
                output += hex(int(tokens[i][1:]))[2:]

        return output


class ArithmaticImmInstruction(Instruction):
    def __init__(self, opcode: str):
        super().__init__(opcode)

    def encode(self, tokens: list[str]) -> str:
        output = ""

        output += hex(int(self.opcode, 2))[2:]

        if tokens[0].startswith("R"):
            output += hex(int(tokens[0][1:]))[2:]

        if tokens[1].startswith("R"):
            output += hex(int(tokens[1][1:]))[2:]

        output += Utils.tohex(int(tokens[2]), 1)

        return output
