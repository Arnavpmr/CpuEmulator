from instruction import Instruction


class Stop(Instruction):
    def __init__(self, opcode: str):
        super().__init__(opcode)

    def encode(self, tokens: list[str]):
        return "0000"
