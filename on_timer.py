import tkinter as Tkinter
from datetime import datetime
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


counter = 0
running = False
welcome_text = 'On Timer!'
stars = '**:**:**'
zeroes = datetime.fromtimestamp(counter).strftime("%H:%M:%S")
save_log = []

if os.path.exists('history.txt'):
    with open('history.txt', 'r') as f:
        history_list = f.readlines()
else:
    history_list = []


def counter_label(widget):
    def count():
        if running:
            global counter
            if counter == 0:
                display = stars
            else:
                tt = datetime.fromtimestamp(counter)
                string = tt.strftime("%H:%M:%S")
                display = string

            widget.config(text=display)
            widget.after(500, count)
            counter += 0.5

    count()


# start function of the stopwatch
def Start(widget):
    global running
    running = True
    counter_label(widget)
    start['state'] = 'disabled'
    stop['state'] = 'normal'
    reset['state'] = 'normal'


# Stop function of the stopwatch
def Stop():
    global running
    start['state'] = 'normal'
    stop['state'] = 'disabled'
    reset['state'] = 'normal'
    running = False


# Reset function of the stopwatch
def Reset(widget):
    global counter
    history.insert(0, datetime.utcnow().strftime("%D") + ': ' + datetime.fromtimestamp(counter).strftime("%H:%M:%S"))
    save_log.append(datetime.utcnow().strftime("%D") + ': ' + datetime.fromtimestamp(counter).strftime("%H:%M:%S"))
    counter = 0

    # If rest is pressed after pressing stop.
    if running == False:
        reset['state'] = 'disabled'
        widget['text'] = zeroes

    # If reset is pressed while the stopwatch is running.
    else:
        widget['text'] = stars


def populate_history(widget):
    global history_list
    for h in history_list:
        widget.insert(0, h)


root = Tkinter.Tk()
root.title("On Timer")
img = Tkinter.PhotoImage(file=resource_path('wall-clock.png'))
root.iconphoto(False, img)
# root.iconbitmap(resource_path('icon.ico'))
# Fixing the window size.
root.minsize(width=250, height=70)
title_label = Tkinter.Label(root, text="On Timer!", fg="black", font="Verdana 10 bold")
title_label.pack()
label = Tkinter.Label(root, text=zeroes, fg="black", bg='white', font="Verdana 24 bold", relief='sunken')
label.pack()
f = Tkinter.Frame(root)
start = Tkinter.Button(f, text='Start', width=6, command=lambda: Start(label))
stop = Tkinter.Button(f, text='Stop', width=6, state='disabled', command=Stop)
reset = Tkinter.Button(f, text='Reset', width=6, state='disabled', command=lambda: Reset(label))
minimize = Tkinter.Button(f, text='Minimize', width=7, command=lambda: root.iconify())
f.pack(anchor='center', pady=5)
start.pack(side="left")
stop.pack(side="left")
reset.pack(side="left")
minimize.pack(side='left')
history = Tkinter.Listbox(height=3, justify='center')
history.pack(fill='both', expand='true')
populate_history(history)
root.mainloop()
with open('history.txt', 'a+') as f:
    for s in save_log:
        f.write("\n%s" % s)