import tkinter as tk
import socket, pickle, PIL.ImageGrab, struct, uuid
import socket, uuid
import os
import keylogger_server as kl 
import app_process_server as ap
import directory_tree_server as dt

main = tk.Tk()
main.geometry("200x200")
main.title("Server")
main['bg'] = 'plum1'

#Global variables
global client
BUFSIZ = 1024 * 4

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
    global client 
    isMod = False
    
    while True:
        if not isMod:
            mod = client.recv(BUFSIZ).decode()

        if (mod == "SHOW"):
            client.sendall("OK".encode())
            while True:
                check = dt.sendListDirs(client)
                if not check[0]:    
                    mod = check[1]
                    if (mod != "error"):
                        isMod = True
                        break
        
        # copy file from client to server
        elif (mod == "COPYTO"):
            client.sendall("OK".encode())
            dt.copyFile(client)
            isMod = False

        # copy file from server to client
        elif (mod == "COPY"):
            client.sendall("OK".encode())
            dt.copyFileTo(client)
            isMod = False

        elif (mod == "DEL"):
            client.sendall("OK".encode())
            dt.delFile(client)
            isMod = False

        else:
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
        elif "SD_LO" in msg:
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

tk.Button(main, text = "OPEN", width = 10, height = 2, fg = 'white', bg = 'IndianRed3', borderwidth=0,
            highlightthickness=0, command = Connect, relief="flat").place(x = 100, y = 100, anchor = "center")
main.mainloop()


