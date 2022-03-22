#for using in ghidra scripting
from binascii import hexlify
from gzip import WRITE
import json
from ast import literal_eval
listing = currentProgram.getListing()
main_func = getGlobalFunctions("init_3")[0] # assume there's only 1 function named 'main'
addrSet = main_func.getBody()
# true means 'forward'

a=addrSet.getMinAddress()
start_m=a.getAddress("08008000")
end_m=a.getAddress("081d67f4")
addrSet.delete(addrSet.getFirstRange())
addrSet.delete(addrSet.getFirstRange())
addrSet.add(start_m,end_m)
codeUnits = listing.getCodeUnits(addrSet, True) 

for codeUnit in codeUnits:
    instruction_data[literal_eval("0x"+"{}".format(codeUnit.getAddress()))]=[codeUnit.toString(),hexlify(codeUnit.getBytes())]
        # can also get bytes of instruction with    hexlify(codeUnit.getBytes())

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