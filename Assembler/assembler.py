import re
from enum import Enum

from branch_instructions import BranchConditional, BranchUnconditional

from arithmatic_instructions import ArithmaticInstruction, ArithmaticImmInstruction
from move import Move, MoveImmediate
from stop import Stop


class AssemblerState(Enum):
    SEARCHING = 1
    SEARCHING_TEXT = 2
    PROCESSING_TEXT = 3
    SEARCHING_DATA = 4
    PROCESSING_DATA = 5
    FINISHED = 6


class Assembler:
    def __init__(self, instructions_file: str) -> None:
        self.pc = 0

        self.instruction_set = {
            "STOP": Stop("0000"),
            "ADD": ArithmaticInstruction("0001"),
            "ADDI": ArithmaticImmInstruction("0010"),
            "SUB": ArithmaticInstruction("0011"),
            "SUBI": ArithmaticImmInstruction("0100"),
            "MUL": ArithmaticInstruction("0101"),
            "MULI": ArithmaticImmInstruction("0110"),
            "DIV": ArithmaticInstruction("0111"),
            "DIVI": ArithmaticImmInstruction("1000"),
            "MOV": Move("1001"),
            "MOVI": MoveImmediate("1010"),
            "LDR": ArithmaticImmInstruction("1011"),
            "STR": ArithmaticImmInstruction("1100"),
            "B": BranchUnconditional("1101"),
            "CBZ": BranchConditional("1110"),
            "CBGZ": BranchConditional("1111")
        }

        self.instructions_file: str = instructions_file
        self.lines: list[str] = []

        self.labels: dict[str, int] = dict()

        self.instruction_data: list[str] = []
        self.data_segment_data: list[str] = []


    def load_file(self):
        self.lines = open(self.instructions_file, "r").readlines()


    def __encode_instruction_tokens(self, tokens: list[str], unprocessed_labels: dict[str, int], unresolved_instructions: dict[str, list[str]], unprocessed_data_labels: dict[str, str]) -> str:
        output = ""

        if tokens[0] == "B":
            if tokens[1] not in self.labels:
                unprocessed_labels[tokens[1]] = self.pc
                unresolved_instructions[tokens[1]] = tokens

                return "0000"

            output += self.instruction_set["B"].encode(tokens[1:], self.labels, self.pc)

        elif tokens[0] == "CBZ" or tokens[0] == "CBGZ":
            if tokens[2] not in self.labels:
                unprocessed_labels[tokens[2]] = self.pc
                unresolved_instructions[tokens[2]] = tokens
                return "0000"

            output += self.instruction_set[tokens[0]].encode(tokens[1:], self.labels, self.pc)

        else:
            output += self.instruction_set[tokens[0]].encode(tokens[1:])

        return output



    def assemble(self):
        state = AssemblerState.SEARCHING

        i = 0

        unresolved_labels: dict[str, int] = {}
        unresolved_instructions: dict[str, list[str]] = {}

        unresolved_data_labels: dict[str, str] = {}

        while state != AssemblerState.FINISHED:
            tokens = self.lines[i].split()

            if not tokens:
                i += 1
                continue

            if state == AssemblerState.SEARCHING:
                if tokens[0] == ".text":
                    state = AssemblerState.PROCESSING_TEXT
                elif tokens[0] == ".data":
                    state = AssemblerState.PROCESSING_DATA

            elif state == AssemblerState.SEARCHING_TEXT:
                if tokens[0] == ".text":
                    state = AssemblerState.PROCESSING_TEXT

            elif state == AssemblerState.SEARCHING_DATA:
                if tokens[0] == ".data":
                    state = AssemblerState.PROCESSING_DATA
                elif i >= len(self.lines) - 1:
                    state = AssemblerState.FINISHED

            elif state == AssemblerState.PROCESSING_TEXT:
                if re.match(r'\w+:', tokens[0]):
                    label_name = tokens[0][:-1]

                    if len(tokens) == 1 or tokens[1].startswith("//"):
                        self.labels[label_name] = self.pc
                        self.pc -= 1
                    else:
                        self.labels[label_name] = self.pc
                        tokens = tokens[1:]

                        self.instruction_data.append(self.__encode_instruction_tokens(tokens, unresolved_labels, unresolved_instructions, unresolved_data_labels))

                    if label_name in unresolved_labels:
                        instruction_id = unresolved_labels[label_name]
                        del unresolved_labels[label_name]

                        self.instruction_data[instruction_id] = self.__encode_instruction_tokens(unresolved_instructions[label_name] + [str(instruction_id)], unresolved_labels, unresolved_instructions, unresolved_data_labels)
                    
                    if tokens[0] == "STOP":
                        if self.data_segment_data:
                            state = AssemblerState.FINISHED
                        else:
                            state = AssemblerState.SEARCHING_DATA


                    self.pc += 1

                elif tokens[0].startswith("//"):
                    i += 1
                    continue

                elif tokens[0] == "STOP" or tokens[0] == ".data":
                    self.instruction_data.append(self.__encode_instruction_tokens(tokens, unresolved_labels, unresolved_instructions, unresolved_data_labels))

                    if self.data_segment_parser.data_segment_data:
                        state = AssemblerState.FINISHED
                    else:
                        state = AssemblerState.SEARCHING_DATA
                else:
                    self.instruction_data.append(self.__encode_instruction_tokens(tokens, unresolved_labels, unresolved_instructions, unresolved_data_labels))
                    self.pc += 1

            elif state == AssemblerState.PROCESSING_DATA:
                if not tokens:
                    i += 1
                    continue                

                if tokens[0].startswith("//"):
                    i += 1
                    continue

                if tokens[0] == ".text":
                    state = AssemblerState.PROCESSING_TEXT
                    i += 1
                    continue

                self.data_segment_data += [data[2:] for data in tokens]

            i += 1

            if i >= len(self.lines):
                state = AssemblerState.FINISHED