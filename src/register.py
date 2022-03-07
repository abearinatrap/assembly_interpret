from bitarray import bitarray

class Register():
    def __init__(self):
        self.registers=[bitarray(32) for i in range(12)]
        self.sp=bitarray(32)
        self.lr=bitarray(32)
        self.psr=bitarray(32)
        self.xpsr=bitarray(32) #flags

        self.registers.append(self.sp)
        self.registers.append(self.lr)
        self.registers.append(self.psr)
        self.registers.append(self.xpsr)