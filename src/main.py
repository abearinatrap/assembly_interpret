#!/usr/bin/env python3
from gzip import WRITE
from bitarray import bitarray
import json
import queue
from src import CPU

class MainApp:
    def __init__(self,guiq,cpuq):
        self.cpu=CPU.CPU()
        self.guiq=guiq
        self.cpuq=cpuq
        self.loadInfo()
        self.running=False

    def loadInfo(self):
        with open("data.json","r") as info_file:
            self.info=json.load(info_file)
        WRITE_LOC="ghidra_data4.json"
        self.current_inst=self.info["entrypoint"]
        with open(WRITE_LOC,"r") as instruction_data_raw:
            self.instruction_data=json.load(instruction_data_raw)

    def execInstr(self):
        self.full_curr_comm=self.instruction_data[str(self.current_inst)][0]
        print(self.full_curr_comm)
        self.curr_data=self.instruction_data[str(self.current_inst)][1]
        print(self.curr_data)
        self.next_inst=self.current_inst+int(len(self.curr_data)/2)
        
        if not self.cpu.run("mov",0,1,2):
            self.info["quit_addr"]=self.current_inst
            self.info["quit_inst"]=self.nstruction_data[self.current_inst]
            #save state here and current instr
            self.info["registers"]=self.cpu.registers
            # how to save memory????
            self.guiq.put_nowait({"type":"fail","address":self.current_inst,"full_command":self.full_curr_comm})
        
        else:
            #instr was successful

            self.guiq.put_nowait({"type":"update","address":self.current_inst,"full_command":self.full_curr_comm})
            pass
        self.current_inst=self.next_inst
    
    def execLoop(self):
        # this is bad.
        while True:
            while True:
                try:
                    msg = self.cpuq.get_nowait()
                except queue.Empty:
                    break
                if msg["type"]=="stop":
                    self.running=False
                elif msg["type"]=="start":
                    self.running=True
                elif msg["type"]=="next":
                    self.execInstr()
                    break
                else:
                    break

                if self.running:
                    self.execInstr()
                


if __name__=="__main__":

    with open("data.json","r") as info_file:
        info=json.load(info_file)

    print(info)
    cpu=CPU.CPU()

    #read instructions
    WRITE_LOC="ghidra_data4.json"
    current_inst=info["entrypoint"]
    print("opening "+WRITE_LOC+" to read instructions. starting at "+str(current_inst))

    with open(WRITE_LOC,"r") as instruction_data_raw:
        instruction_data=json.load(instruction_data_raw)
    #get instruction data
    #print(instruction_data[current_inst])
    curr_comm=instruction_data[str(current_inst)][0]
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