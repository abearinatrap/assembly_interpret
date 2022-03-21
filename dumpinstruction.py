#for using in ghidra scripting
from binascii import hexlify
from gzip import WRITE
import json

listing = currentProgram.getListing()
main_func = getGlobalFunctions("main")[0] # assume there's only 1 function named 'main'
addrSet = main_func.getBody()
codeUnits = listing.getCodeUnits(addrSet, True) # true means 'forward'



for codeUnit in codeUnits:
    #codeUnit.toString() is the command
    #print("0x{} : {:16} {}".format(codeUnit.getAddress(), hexlify(codeUnit.getBytes()), codeUnit.toString()))
    instruction_data[codeUnit.getAddress()]=codeUnit.toString()

WRITE_LOC="C:/dev2/ghidra_data.json"

print(str(len(instruction_data))+" instructions written to "+WRITE_LOC)

with open(WRITE_LOC,"w+") as write_file:
    json.dump(instruction_data,write_file)


function_data={}
func = getFirstFunction()
while func is not None:
    function_data[func.getName()]="{}".format(func.getEntryPoint())
    func = getFunctionAfter(func)
WRITE_func_LOC="C:/dev2/ghidra_function_data.json"
with open(WRITE_func_LOC,"w+") as write_file:
    json.dump(function_data,write_file)

instruction_data={}
listing = currentProgram.getListing()
for func in function_data:
    if len(getGlobalFunctions(func))==0: 
        continue
    curr_func = getGlobalFunctions(func)[0] # assume there's only 1 function named what the function is
    addrSet = curr_func.getBody()
    codeUnits = listing.getCodeUnits(addrSet, True) # true means 'forward'
    for codeUnit in codeUnits:
        instruction_data[literal_eval("0x"+"{}".format(codeUnit.getAddress()))]=[codeUnit.toString(),hexlify(codeUnit.getBytes())]
        # can also get bytes of instruction with    hexlify(codeUnit.getBytes())
WRITE_LOC="C:/dev2/ghidra_data3.json"
with open(WRITE_LOC,"w+") as write_file:
    json.dump(instruction_data,write_file)