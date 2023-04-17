from tkinter import *
from tkinter.ttk import Combobox
from pynput.mouse import Controller, Button as MouseButton
import time
import threading

root = Tk()
mouse = Controller()

# window settings
root.title('Simple Auto Clicker')
root.resizable(width=False, height=False)
root.iconbitmap('./assets/favicon.ico')
root.attributes('-topmost', 1)

window_width = 380
window_height = 300

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# global container
GlobalContainer = Frame(
    root,
    padx=10,
    pady=10
)
GlobalContainer.pack(
    fill=BOTH,
    expand=1
)

# first row of the interface
FirstRowContainer = Frame(GlobalContainer)
FirstRowContainer.pack(
    fill=BOTH,
    expand=1
)

# interval container
IntervalContainer = LabelFrame(
    FirstRowContainer,
    text='Interval',
    border=1,
    relief='solid'
)
IntervalContainer.pack(side=LEFT)

IntervalInputContainer = Frame(
    IntervalContainer,
    padx=10,
    pady=10
)
IntervalInputContainer.pack()

clicksPerSecond = IntVar(IntervalInputContainer, value=1)
IntervalInput = Spinbox(
    IntervalInputContainer,
    width=5,
    from_=1,
    to=10,
    textvariable=clicksPerSecond
)
IntervalInput.pack(side=LEFT)

IntervalInputLabel = Label(
    IntervalInputContainer,
    text='clicks per seconds'
)
IntervalInputLabel.pack(side=LEFT)

# click options container
ClickOptionsContainer = LabelFrame(
    FirstRowContainer,
    text='Click options',
    border=1,
    relief='solid'
)
ClickOptionsContainer.pack(side=RIGHT)

ClickOptionsInputContainer = Frame(
    ClickOptionsContainer,
    padx=10,
    pady=10
)
ClickOptionsInputContainer.pack()

ClickOptionsInputLabel = Label(
    ClickOptionsInputContainer,
    text='Mouse button: '
)
ClickOptionsInputLabel.pack(side=LEFT)

selectedMouseButton = StringVar(ClickOptionsInputContainer, value='left')
ClickOptionsInput = Combobox(
    ClickOptionsInputContainer,
    textvariable=selectedMouseButton,
    values=['left', 'right', 'middle'],
    state='readonly',
    width=6
)
ClickOptionsInput.pack(side=LEFT)


# second row of the interface
SecondRowContainer = Frame(GlobalContainer)
SecondRowContainer.pack(
    fill=BOTH,
    expand=1
)

CursorPositionContainer = LabelFrame(
    SecondRowContainer,
    text='Cursor position',
    border=1,
    relief='solid'
)
CursorPositionContainer.pack(fill=BOTH, expand=1)

CursorPositionInputXContainer = Frame(
    CursorPositionContainer,
    padx=10,
    pady=10
)
CursorPositionInputXContainer.pack(side=LEFT)

CursorPositionInputXLabel = Label(
    CursorPositionInputXContainer,
    text='X: '
)
CursorPositionInputXLabel.pack(side=LEFT)

mouseX = StringVar(CursorPositionInputXContainer, value='')
CursorPositionXInput = Entry(
    CursorPositionInputXContainer,
    width=5,
    textvariable=mouseX,
    state='readonly'
)
CursorPositionXInput.pack(side=LEFT)

CursorPositionInputYContainer = Frame(
    CursorPositionContainer,
    padx=10,
    pady=10
)
CursorPositionInputYContainer.pack(side=LEFT)

CursorPositionInputYLabel = Label(
    CursorPositionInputYContainer,
    text='Y: '
)
CursorPositionInputYLabel.pack(side=LEFT)

mouseY = StringVar(CursorPositionInputYContainer, value='')
CursorPositionYInput = Entry(
    CursorPositionInputYContainer,
    width=5,
    textvariable=mouseY,
    state='readonly'
)
CursorPositionYInput.pack(side=LEFT)

# third row of the interface
ThirdRowContainer = Frame(GlobalContainer)
ThirdRowContainer.pack(
    fill=BOTH,
    expand=1
)

StartButton = Button(
    ThirdRowContainer,
    text='Start',
    padx=70,
    pady=30,
    command=lambda: startStopClicker('<F9>'),
)
StartButton.pack(side=LEFT)

StopButton = Button(
    ThirdRowContainer,
    text='Stop',
    padx=70,
    pady=30,
    state='disabled',
    command=lambda: startStopClicker('<F9>'),
)
StopButton.pack(side=RIGHT)

# functions
autoClickerRunning = False


def autoClickerLoop():
    global autoClickerRunning, mouseX, mouseY

    while autoClickerRunning:
        print('click')

        mouseX.set(mouse.position[0])
        mouseY.set(mouse.position[1])

        mouse.click(MouseButton[selectedMouseButton.get()], 1)
        time.sleep(1/clicksPerSecond.get())

autoClickerThread = threading.Thread(target=autoClickerLoop)


def startStopClicker(event):
    global autoClickerRunning, autoClickerThread

    print(event)
    if autoClickerRunning:  # if the auto clicker is running
        print('stop')
        StopButton['state'] = ['disabled']
        StartButton['state'] = ['normal']
        autoClickerRunning = False

        autoClickerThread.run()
        
    else:  # if the auto clicker is not running
        print('start')
        StopButton['state'] = ['normal']
        StartButton['state'] = ['disabled']
        autoClickerRunning = True

        autoClickerThread.start()


def exitProgram(event):
    global autoClickerThread
    
    autoClickerThread.run()
    root.destroy()


# keybinds
root.bind('<Escape>', exitProgram)
root.bind('<F9>', startStopClicker)

root.mainloop()
