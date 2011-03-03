from Tkinter import *

class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"
        
    def say_neu(self):
        print "neu!!!"

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack({"side": "left"})
        
        self.neuerButton = Button(self)
        self.neuerButton["text"] = "Neu"
        self.neuerButton["command"] = self.say_neu
        self.neuerButton.pack({"side" : "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
