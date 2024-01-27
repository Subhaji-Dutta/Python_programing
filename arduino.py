from pyfirmata import Arduino
import time
import threading
import tkinter as tk
from pynput.keyboard import Key, Listener

board= Arduino('COM5')

pin_3 = board.get_pin('d:3:p')
pin_6 = board.get_pin('d:6:p')
pin_2 = board.get_pin('d:2:o')
pin_4 = board.get_pin('d:4:o')
pin_5 = board.get_pin('d:5:o')
pin_7 = board.get_pin('d:7:o')

speed = 0.6

def forward():
    global speed
    pin_3.write(speed)
    pin_5.wirte(1)
    pin_7.write(0)
    pin_6.write(speed)
    pin_4.write(0)
    pin_2.write(1)

def stop():
    pin_3.write(0)
    pin_5.wirte(0)
    pin_7.write(0)
    pin_6.write(0)
    pin_4.write(0)
    pin_2.write(0)

value = ''
value2 = ''
def on_press(Key):
    global value
    global value2
    try:
        if Key.char == 'w':
            value= 1
            forward()
        else:
            stop()
    except:
        stop()

def on_release(Key):
    global value
    global value2
    try: 
        if Key.char =='w':
            value=0
            stop()
        else:
            stop()
    except:
        stop()

def get_keys():
    with Listener(
        on_press= on_press,
        on_release= on_release)as listener:
        listener.join()

thread1 = threading.Thread(target=get_keys)
thread1.start()
