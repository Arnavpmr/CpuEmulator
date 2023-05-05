import unittest
from assembler import Assembler

class AssemblerTest(unittest.TestCase):
    def test_load_file(self):
        assembler = Assembler("test_instructions.txt")
        assembler.load_file()
        self.assertEqual(assembler.instruction_data, ['0x10', '0x20', '0x30'])

    def test_assemble(self):
        assembler = Assembler("test_instructions.txt")
        assembler.load_file()
        assembler.assemble()
        self.assertEqual(assembler.assembled_instructions, ['1000', '2000', '3000'])

    def test_write_instructions_file(self):
        assembler = Assembler("test_instructions.txt")
        assembler.load_file()
        assembler.assemble()
        assembler.write_instructions_file("test_instructions.o")
        with open("test_instructions.o", "r") as f:
            file_data = f.read()
            self.assertEqual(file_data, "v3.0 hex words addressed\n0000: 1000 2000 3000")

    def test_write_data_file(self):
        assembler = Assembler("test_instructions.txt", "test_data.txt")
        assembler.load_file()
        assembler.assemble()
        assembler.write_data_file("test_data.o")
        with open("test_data.o", "r") as f:
            file_data = f.read()
            self.assertEqual(file_data, "v3.0 hex words addressed\n0000: 0001 0002 0003")

if __name__=="__main__":
    unittest.main()
