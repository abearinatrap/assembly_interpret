from bitarray import bitarray

class Register():
    def __init__(self):
        self.data=bitarray('0'*32,endian='little')
    