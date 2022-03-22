#!/usr/bin/env python3
from gzip import WRITE
from bitarray import bitarray
import json
from src import CPU

if __name__=="__main__":

    with open("data.json","r") as info_file:
        info=json.load(info_file)

    print(info)
    cpu=CPU.CPU()

    #read instructions
    WRITE_LOC="ghidra_data3.json"
    current_inst=info["entrypoint"]
    print("opening "+WRITE_LOC+" to read instructions. starting at "+str(current_inst))

    with open(WRITE_LOC,"r") as instruction_data_raw:
        instruction_data=json.load(instruction_data_raw)
    #get instruction data
    print(instruction_data[current_inst])
    curr_comm=instruction_data[current_inst][0].split()[0]
    print(curr_comm)

    if not cpu.run("mov",0,1,2):
        info["quit_addr"]=current_inst
        info["quit_inst"]=instruction_data[current_inst]
        #save state here and current instr
        info["registers"]=cpu.registers
        # how to save memory????
        pass
    else:
        #instr was successful
        pass

    here=input()    