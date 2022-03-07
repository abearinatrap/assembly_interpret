from bitarray import bitarray

class Register():
    def __init__(self):
        self.data=bitarray(32)
        self.data.setall(0)

