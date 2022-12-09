from utils import Utils

from instruction import Instruction

class Move(Instruction):
    def __init__(self, opcode: str):
        super().__init__(opcode)

    def encode(self, tokens: list[str]):
        output = ""

        output += hex(int(self.opcode, 2))[2:]

        if tokens[0].startswith("R"):
            output += Utils.tohex(int(tokens[0][1:]), 1)

        if tokens[1].startswith("R"):
            output += Utils.tohex(int(tokens[1][1:]), 1)

        output += "0"

        return output


class MoveImmediate(Instruction):
    def __init__(self, opcode: str):
        super().__init__(opcode)

    def encode(self, tokens: list[str]):
        output = ""

        output += hex(int(self.opcode, 2))[2:]

        if tokens[0].startswith("R"):
            output += Utils.tohex(int(tokens[0][1:]), 1)

        output += Utils.tohex(int(tokens[1]), 2)

        return output
