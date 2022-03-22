from bitarray import bitarray
import json
from .register import Register

class CPU():
    def __init__(self):
        '''Emulator of 32-bit ARM Cortex M7 used in Pixhawk 4'''
        self.registers=[Register() for i in range(12)]
        self.sp=Register()
        self.lr=Register()
        self.psr=Register()
        self.xpsr=Register() #flags
        self.stack=[]
        self.stack_addr=0

        self.registers.append(self.sp)
        self.registers.append(self.lr)
        self.registers.append(self.psr)
        self.registers.append(self.xpsr)

        self.memory = bitarray(30000000)

    def run(self,instr,*args):
        #run instruction, given name
        if getattr(self,instr,None)==None:
            #instruction not found, throw error and save state
            return False
        getattr(self,instr,None)(*args)
        return True

    def mov(self,*args):
        mode,d,s=args
        if mode==0:
            # direct:direct
            self.registers[d]=self.registers[s]
        elif mode==1:
            # direct:indirect
            pass
        elif mode==2:
            # indirect:direct
            pass
        elif mode==3:
            # indirect:indirect
            pass
        elif mode==4:
            # literal
            self.registers[d]=s
    