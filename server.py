import tkinter as tk
<<<<<<< HEAD
import socket, uuid
import os
import keylogger_server as kl 
import app_process_server as ap
=======
import socket, pickle, PIL.ImageGrab, psutil, struct, uuid
import os, json, re, winreg, threading, subprocess
import numpy as np
from pynput.keyboard import Listener
import keylogger_server as kl 
>>>>>>> f545b813dac6a133a16b8232c4961e85e6242301

main = tk.Tk()
main.geometry("200x200")
main.title("Server")
<<<<<<< HEAD
main['bg'] = 'plum1'

#Global variables
global client
BUFSIZ = 1024 * 4

=======

#Global variables
###############################################################################
global client
BUFSIZ = 1024 * 4
WIDTH = 1900
HEIGHT = 1000
###############################################################################
>>>>>>> f545b813dac6a133a16b8232c4961e85e6242301
def keylogger():
    global client
    kl.keylog(client)
    return

def shutdown_logout():
    msg = client.recv(BUFSIZ).decode("utf8")
    if "SHUTDOWN" in msg:
        os.system('shutdown -s -t 15')
    elif "LOGOUT" in msg:
        os.system('shutdown -l')
    return

def mac_address():
    global client
    client.sendall(bytes(hex(uuid.getnode()), "utf8"))
    return

def app_process():
<<<<<<< HEAD
    global client
    ap.app_process(client)
=======
>>>>>>> f545b813dac6a133a16b8232c4961e85e6242301
    return

def live_screen():
    return

def directory_tree():
    return
#Connect
###############################################################################           
def Connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ''
    port = 5656
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(100)
    global client
    client, addr = s.accept()
    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        if "KEYLOG" in msg:
            keylogger()
<<<<<<< HEAD
        elif "SD_LO" in msg:
            shutdown_logout()
        elif "LIVESCREEN" in msg:
            live_screen()
        elif "APP_PRO" in msg:
=======
        elif "SHUTDOWN" in msg:
            shutdown_logout()
        elif "LIVESCREEN" in msg:
            live_screen()
        elif "PROCESS" in msg:
>>>>>>> f545b813dac6a133a16b8232c4961e85e6242301
            app_process()
        elif "MAC" in msg:
            mac_address()
        elif "DIRECTORY" in msg:
            directory_tree()
        elif "QUIT" in msg:
            client.close()
            s.close()
            return
###############################################################################    

<<<<<<< HEAD
tk.Button(main, text = "OPEN", width = 10, height = 2, fg = 'white', bg = 'IndianRed3', borderwidth=0,
            highlightthickness=0, command = Connect, relief="flat").place(x = 100, y = 100, anchor = "center")
=======
tk.Button(main, text = "Open", command = Connect).place(x = 100, y = 100, anchor = "center")

>>>>>>> f545b813dac6a133a16b8232c4961e85e6242301
main.mainloop()


