from tkinter import *
from tkinter import messagebox
import threading
from multiprocessing import Queue, Process

clientRunning = False
window = Tk()
window.title("Client GUI")
window.geometry('350x350')
lbl = Label(window, text="Hello")
lbl.grid(column=0, row=0)

serverLbl = Label(window, text="Server Address: ")
serverLbl.grid(column=0, row=2)

portLbl = Label(window, text="Port Address: ")
portLbl.grid(column=0, row=3)

powerLbl = Label(window, text="Power In Address: ")
powerLbl.grid(column=0, row=5)

currentLbl = Label(window, text="Current In Address: ")
currentLbl.grid(column=0, row=6)
chargeLbl = Label(window, text="Charge Address: ")
chargeLbl.grid(column=0, row=7)

serverTxt = Entry(window, width=10)
serverTxt.grid(column=1, row=2)

powerTxt = Entry(window, width=10)
powerTxt.grid(column=1, row=5)

currentTxt = Entry(window, width=10)
currentTxt.grid(column=1, row=6)

chargeTxt = Entry(window, width=10)
chargeTxt.grid(column=1, row=7)

portTxt = Entry(window, width=10)
portTxt.grid(column=1, row=3)

canvas = Canvas(window, width=20, height=20)
canvas.grid(column=1, row=4)

canvasMaster = Canvas(window, width=20, height=20)
canvasMaster.grid(column=1, row=8)


def create_circle(x, y, r, canvasName, fill):  # center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill=fill, outline=fill)


create_circle(10, 10, 5, canvas, "red")
create_circle(10, 10, 5, canvasMaster, "red")


def startclicked():
    global clientRunning
    clientRunning = True
    print("Starting Client")
    add = serverTxt.get()
    port = portTxt.get()
    if add == "":
        add = "localhost"
        serverTxt.insert(0, add)
    if port == "":
        port = 5021
        portTxt.insert(0, port)
    else:
        port = int(port)
    create_circle(10, 10, 5, canvas, "green")
    th = threading.Thread(target=runserver, args=(add, port))
    th.start()


def runserver(add, port):
    print(add, port)
    from client import run_server
    run_server(add, port)


def startMaster():
    if not clientRunning:
        messagebox.showerror("Master Error", "Client not running!")
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
        powerTxt.insert(0, power)
    else:
        power = int(power)
    if current == "":
        current = 204
        currentTxt.insert(0, current)
    else:
        current = int(current)
    if charge == "":
        charge = 206
        chargeTxt.insert(0, charge)
    else:
        charge = int(charge)
    queue = Queue()

    th = threading.Thread(target=runmaster, args=(add, port, power, current, charge, queue))
    th.start()


Label(window, text="Power Result: ").grid(column=0, row=9)
Label(window, text="Current Result: ").grid(column=0, row=10)
Label(window, text="Charge Result: ").grid(column=0, row=11)

pR = Label(window, text="")
pR.grid(column=1, row=9)
cuR = Label(window, text="")
cuR.grid(column=1, row=10)
chR = Label(window, text="")
chR.grid(column=1, row=11)


def runmaster(add, port, power, current, charge, queue):
    from master import run_master
    run_master(add, port, power, current, charge, queue)
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
                r3 = str(int(r3) / 100) + '%'
                cuR.config(text=r2)

                chR.config(text=r3)


startButton = Button(window, text="Start Client", command=startclicked)
startButton.grid(column=0, row=4)

startMasterB = Button(window, text="Start Master", command=startMaster)
startMasterB.grid(column=0, row=8)

window.mainloop()
