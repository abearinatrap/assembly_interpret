from email import message
import tkinter as tk
import tkinter.font as tkFont
import threading
import queue
from src import CPU
from src.main import MainApp
import json
#i hate oop i hate oop i hate oop i hate oop

#define queues for communication both ways
guiQueue=queue.Queue()
cpuQueue=queue.Queue()

class App:
    def __init__(self, root,guiq,cpuq,initdatafunc):
        #setting title
        root.title("undefined")
        self.guiq=guiq
        self.cpuq=cpuq
        self.flowInstr=False
        self.checkSpeed=100
        self.initdatafunc=initdatafunc
        #setting window size
        self.width=600
        self.height=500
        self.screenwidth = root.winfo_screenwidth()
        self.screenheight = root.winfo_screenheight()
        self.alignstr = '%dx%d+%d+%d' % (self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2)
        root.geometry(self.alignstr)
        root.resizable(width=False, height=False)

        self.GLabel_52=tk.Label(root)
        ft = tkFont.Font(family='Times',size=22)
        self.GLabel_52["font"] = ft
        self.GLabel_52["fg"] = "#333333"
        self.GLabel_52["justify"] = "center"
        self.GLabel_52["text"] = "CPU Emulator"
        self.GLabel_52.place(x=210,y=30,width=180,height=30)

        self.GButton_526=tk.Button(root)
        self.GButton_526["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        self.GButton_526["font"] = ft
        self.GButton_526["fg"] = "#000000"
        self.GButton_526["justify"] = "center"
        self.GButton_526["text"] = "Next Instruction"
        self.GButton_526.place(x=220,y=430,width=138,height=30)
        self.GButton_526["command"] = self.GButton_526_command

        self.GCheckBox_384=tk.Checkbutton(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GCheckBox_384["font"] = ft
        self.GCheckBox_384["fg"] = "#333333"
        self.GCheckBox_384["justify"] = "center"
        self.GCheckBox_384["text"] = "Continue (stops on error)"
        self.GCheckBox_384.place(x=180,y=390,width=218,height=30)
        self.GCheckBox_384["offvalue"] = "0"
        self.GCheckBox_384["onvalue"] = "1"
        self.GCheckBox_384["command"] = self.GCheckBox_384_command
        self.checkboxValue=tk.IntVar()
        self.GCheckBox_384["variable"]=self.checkboxValue

        self.GMessage_287=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GMessage_287["font"] = ft
        self.GMessage_287["fg"] = "#333333"
        self.GMessage_287["justify"] = "center"
        self.GMessage_287["text"] = "Current Data"
        self.GMessage_287["relief"] = "sunken"
        self.GMessage_287.place(x=220,y=140,width=278,height=145)

        self.GLabel_693=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_693["font"] = ft
        self.GLabel_693["fg"] = "#333333"
        self.GLabel_693["justify"] = "center"
        self.GLabel_693["text"] = "Current Data:"
        self.GLabel_693.place(x=140,y=200,width=87,height=30)

        self.GButton_260=tk.Button(root)
        self.GButton_260["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        self.GButton_260["font"] = ft
        self.GButton_260["fg"] = "#000000"
        self.GButton_260["justify"] = "center"
        self.GButton_260["text"] = "Load Data"
        self.GButton_260.place(x=60,y=30,width=105,height=30)
        self.GButton_260["command"] = self.GButton_260_command

    def setMessage(self,message):
        self.GMessage_287["text"]=message

    def GButton_526_command(self):
        if self.checkboxValue.get():
            if self.flowInstr:
                self.cpuq.put_nowait({"type":"stop"})
            else:
                self.cpuq.put_nowait({"type":"start"})
            self.flowInstr=not self.flowInstr
        else:
            self.cpuq.put_nowait({"type":"next"})

    
    def GCheckBox_384_command(self):
        if self.checkboxValue.get():
            #print("checked")
            self.GButton_526["text"] = "Toggle flow"
        else:
            #print("unchecked")
            self.GButton_526["text"] = "Next Instruction"
            self.cpuq.put_nowait({"type":"stop"})

    def GButton_260_command(self):
        self.initdatafunc()


if __name__ == "__main__":
    main=MainApp(guiQueue,cpuQueue)
    root = tk.Tk()
    app = App(root,guiQueue,cpuQueue,main.loadInfo)
    def periodicCheck():
        try:
            message=app.guiq.get_nowait()
            if message.get("type")=="update":
                app.setMessage(str(hex(message["address"]))+": "+str(message["full_command"]))
            elif message.get("type")=="fail":
                app.setMessage("Failed on "+str(hex(message["address"]))+": "+str(message["full_command"]))
        except queue.Empty:
            pass
        root.after(app.checkSpeed,periodicCheck)
    
    threading.Thread(target=main.execLoop, daemon=True).start()
    periodicCheck()
    root.mainloop()