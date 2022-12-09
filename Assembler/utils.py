class Utils:
    @staticmethod
    def tohex(num: int, numdigits: int):
        if num >= 0:
            output = "{:0" + str(numdigits) + "}"

            return output.format(num)
        else:
            return hex(num & (2**(4*numdigits) - 1))[2:]
