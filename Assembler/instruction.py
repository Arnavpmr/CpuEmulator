class Instruction:
    def __init__(self, opcode: str):
        self.opcode = opcode

    def encode(self, tokens: list[str], labels: dict[str, int], pc: int) -> str:
        return "0000"
