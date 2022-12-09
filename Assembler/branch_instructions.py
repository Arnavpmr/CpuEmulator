from utils import Utils

class BranchingInstruction:
    def __init__(self, opcode: str) -> None:
        self.opcode = opcode

    def encode(self, tokens: list[str], labels: dict[str, int], pc: int) -> str:
        return "0000"

class BranchUnconditional(BranchingInstruction):
    def __init__(self, opcode: str):
        super().__init__(opcode)

    def encode(self, tokens: list[str], labels: dict[str, int], pc: int):
        output = ""

        output += hex(int(self.opcode, 2))[2:]

        offset = 0

        if len(tokens) > 1:
            offset = labels[tokens[0]] - int(tokens[1])
        else:
            offset = labels[tokens[0]] - pc


        output += Utils.tohex(offset, 3)

        return output

class BranchConditional(BranchingInstruction):
    def __init__(self, opcode: str):
        super().__init__(opcode)

    def encode(self, tokens: list[str], labels: dict[str, int], pc: int):
        output = ""

        output += hex(int(self.opcode, 2))[2:]

        if tokens[0].startswith("R"):
            output += hex(int(tokens[0][1:]))[2:]

        if len(tokens) > 2:
            offset = labels[tokens[1]] - int(tokens[2])
        else:
            offset = labels[tokens[1]] - pc

        output += Utils.tohex(offset, 2)

        return output
