from assembler import Assembler
import argparse


def main():
    parser = argparse.ArgumentParser(
                    prog='Assembler',
                    description='This program compiles assembl',
                    epilog='Text at the bottom of help')
    
    parser.add_argument('instructionsfilename')
    parser.add_argument('datafilename')

    args = parser.parse_args()

    print(args.instructionsfilename)

    assembler = Assembler(parser.instructionsfilename)

    assembler.load_file()
    assembler.assemble()

    header = "v3.0 hex words addressed"

    instructions_file = open("instructions.o", "w")

    instructions_file.write(header + "\n")
    instructions_file.write("0000: " + " ".join(assembler.instruction_data))

    instructions_file.close()


    datasegment_file = open("data.o", "w")

    datasegment_file.write(header + "\n")
    datasegment_file.write("0000: " + " ".join(assembler.data_segment_data))

    datasegment_file.close()


if __name__ == "__main__":
    main()
