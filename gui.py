from tkinter import *
from tkinter import messagebox
import threading
from multiprocessing import Queue,Process

inputType = "default"
stopThread = False

clientRunning = False
window = Tk()
window.title("Client GUI")
window.geometry('500x350')
lbl = Label(window,text="Hello")
lbl.grid(column = 0, row = 0, columnspan = 7)

serverLbl = Label(window,text="Server Address: ")
serverLbl.grid(column = 0, row =1)

portLbl = Label(window,text="Port Address: ")
portLbl.grid(column = 0, row = 2)

powerLbl = Label(window,text="Power In Address: ")
powerLbl.grid(column = 4, row = 1)

currentLbl = Label(window,text="Current In Address: ")
currentLbl.grid(column = 4,row=2)
chargeLbl = Label(window,text="Charge Address: ")
chargeLbl.grid(column = 4, row = 3)


serverTxt = Entry(window,width=10)
serverTxt.grid(column = 1, row = 1)

powerTxt = Entry(window,width=10)
powerTxt.grid(column = 5,row = 1)

currentTxt = Entry(window,width = 10)
currentTxt.grid(column = 5, row = 2)

chargeTxt = Entry(window,width=10)
chargeTxt.grid(column = 5, row = 3)

portTxt = Entry(window,width=10)
portTxt.grid(column = 1, row = 2)

canvas = Canvas(window,width=20,height=20)
canvas.grid(column=1,row=3)

canvasMaster = Canvas(window, width=20,height=20)
canvasMaster.grid(column=5,row=4)


def create_circle(x, y, r, canvasName,fill): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1,fill=fill,outline=fill)

create_circle(10,10,5,canvas,"red")
create_circle(10,10,5,canvasMaster,"red")
def startclicked():
    global stopThread
    print(stopThread)

    if not stopThread:


        stopThread = True
        create_circle(10, 10, 5, canvas, "red")
        global clientRunning
        clientRunning = True
        print("Starting Client")
        add = serverTxt.get()
        port = portTxt.get()
        if add == "":
            add = "localhost"
            serverTxt.insert(0,add)
        if port == "":
            port = 5021
            portTxt.insert(0,port)
        else:
            port = int(port)
        create_circle(10, 10, 5, canvas, "green")
        runserver(add,port)
    else:
        messagebox.showerror("Client Error", "Client already running!")


def runserver(add,port):
    global inputType

    print(add,port)
    from client import run_server
    th = threading.Thread(target=run_server, args=(add, port, inputType))
    th.start()




def startMaster():
    if not clientRunning:
        messagebox.showerror("Master Error","Client not running!")
        return

    create_circle(10, 10, 5, canvasMaster, "green")
    print("Starting Master")
    add = serverTxt.get()
    port = portTxt.get()
    if add == "":
        add = "localhost"
        serverTxt.set()
    if port == "":
        port = 5021
    else:
        port = int(port)
    power = powerTxt.get()
    current = currentTxt.get()
    charge = chargeTxt.get()

    if power == "":
        power = 202
        powerTxt.insert(0,power)
    else: power = int(power)
    if current == "":
        current = 204
        currentTxt.insert(0,current)
    else: current = int(current)
    if charge == "":
        charge = 206
        chargeTxt.insert(0,charge)
    else: charge = int(charge)
    queue = Queue()

    th = threading.Thread(target = runmaster,args = (add,port,power,current,charge,queue))
    th.start()

Label(window,text="Power Result: ").grid(column = 4, row = 5)
Label(window,text="Current Result: ").grid(column = 4, row = 6)
Label(window,text="Charge Result: ").grid(column = 4, row = 7)

pR = Label(window,text="")
pR.grid(column = 5, row = 5)
cuR = Label(window,text="")
cuR.grid(column = 5, row = 6)
chR = Label(window,text="")
chR.grid(column = 5, row = 7)



def runmaster(add,port,power,current,charge,queue):
    from master import run_master
    run_master(add,port,power,current,charge,queue)
    while not queue.empty():
        response = queue.get()
        print(response)
        if response == "done":
            create_circle(10, 10, 5, canvasMaster, "red")
            while not queue.empty():
                r1 = queue.get()
                pR.config(text=r1)
                r2 = queue.get()
                r3 = queue.get()
                r3 = str(int(r3)/100) + '%'
                cuR.config(text=r2)

                chR.config(text=r3)


simCanvas = Canvas(window, width=20,height=20)
simCanvas.grid(column=1,row=7)
create_circle(10,10,5,simCanvas,"red")

randomCanvas = Canvas(window, width=20,height=20)
randomCanvas.grid(column=1,row=5)
create_circle(10,10,5,randomCanvas,"red")

jsonCanvas = Canvas(window, width=20,height=20)
jsonCanvas.grid(column=1,row=6)
create_circle(10,10,5,jsonCanvas,"red")

def randomClicked():
    create_circle(10, 10, 5, randomCanvas, "green")
    create_circle(10, 10, 5, jsonCanvas, "red")
    create_circle(10, 10, 5, simCanvas, "red")
    global inputType
    inputType = "rand"

def jsonClicked():
    create_circle(10, 10, 5, randomCanvas, "red")
    create_circle(10, 10, 5, jsonCanvas, "green")
    create_circle(10, 10, 5, simCanvas, "red")
    global inputType
    inputType = "json"



def simulateClicked():
    create_circle(10, 10, 5, randomCanvas, "red")
    create_circle(10, 10, 5, jsonCanvas, "red")
    create_circle(10, 10, 5, simCanvas, "green")
    global inputType
    inputType = "simu"

startButton = Button(window,text="Start Client", command=startclicked)
startButton.grid(column = 0, row = 3)


def stopClicked():
    global window
    window.destroy()

    sys.exit(0)

startMasterB = Button(window,text="Start Master",command=startMaster)
startMasterB.grid(column = 4, row = 4)

randomButton = Button(window,text="Random",command=randomClicked)
randomButton.grid(column = 0, row = 5)

jsonButton = Button(window,text="JSON/CSV",command=jsonClicked)
jsonButton.grid(column = 0, row = 6)

simulateButton = Button(window,text="Simulate",command=simulateClicked)
simulateButton.grid(column = 0, row = 7)

stopButton  = Button(window,text="Stop Client",command =stopClicked)
stopButton.grid(column = 0, row = 4)







window.mainloop()




