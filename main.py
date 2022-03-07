#!/usr/bin/env python3
from src import Register
from bitarray import bitarray
import json

class CPU():
    def __init__(self):
        self.registers=[Register() for i in range(12)]
        self.sp=Register()
        self.lr=Register()
        self.psr=Register()
        self.xpsr=Register() #flags

        self.registers.append(self.sp)
        self.registers.append(self.lr)
        self.registers.append(self.psr)
        self.registers.append(self.xpsr)

        self.memory = bitarray(1000000000)



if __name__=="__main__":

    with open("data.json","r") as info_file:
        info=json.load(info_file)

    
    cpu=CPU()
    here=input()    