import requests
import sys, threading
from pynput import keyboard
import tkinter as tk
from tkinter import ttk

if len(sys.argv) > 1:
    # usb tether
    urlVolUp = "http://192.168.42.214:9000/volume-up"
    urlVolDown = "http://192.168.42.214:9000/volume-down"
else:
    urlVolUp = "http://192.168.0.91:9000/volume-up"
    urlVolDown = "http://192.168.0.91:9000/volume-down"

#Android volume indicator
root = tk.Tk()
root.overrideredirect(1)
root.geometry("100x60+100+10")
progressBar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=100, mode="determinate")
progressBar.pack()
labelText = tk.StringVar()
label = tk.Label(root, textvariable=labelText)
label.pack(pady=10)
root.withdraw()

timer = None
timerLock = threading.Lock()
def scheduleHideGUI(waitTimeSec):
    global timer
    global timerLock
    with timerLock:
        if timer:
            timer.cancel()
        timer = threading.Timer(waitTimeSec, lambda : root.withdraw())
        timer.start()
    
def changeVol(url):
    global progressBar
    try:
        r = requests.get(url=url)
        vol = list(map(lambda s: int(s), r.text.split()))
    except ValueError:
        print("Not number. Text received:", r.text)
        return
    except Exception as err:
        print("GET err: ", err)
        return
    if len(vol) != 2:
        print("Should have 2 numbers. Text received:", r.text)
        return
        
    progressBar["value"] = vol[0]
    progressBar["maximum"] = vol[1]
    labelText.set(f"Vol: {vol[0]} / {vol[1]}")
    root.deiconify()
    scheduleHideGUI(2)

def onPress(key):
    # Mouse key G8
    if key == keyboard.Key.f15:
        changeVol(urlVolUp)
    elif key == keyboard.Key.f14:
        changeVol(urlVolDown)

listener = keyboard.Listener(on_press=onPress)
listener.start()

#Android volume indicator
root.mainloop()