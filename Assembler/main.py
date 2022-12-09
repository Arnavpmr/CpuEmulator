from assembler import Assembler


def main():
    assembler = Assembler("instructions.s")

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
