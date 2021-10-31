import entrance_ui as ui1
import main_ui as ui2
import socket
import tkinter as tk
import shutdown_logout_client as sl
import mac_address_client as mac
import keylogger_client as kl
import app_process_client as ap

#global variables
BUFSIZ = 1024 * 4
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
root = tk.Tk()
root.geometry("1000x600")
root.configure(bg = "#FFFFFF")
root.resizable(False, False)
f1 = ui1.Entrance_UI(root)

def back(ui):
    ui.place_forget()
    f2.place(x = 0, y = 0)
    client.sendall(bytes("QUIT", "utf8"))

def live_screen():
    return

def shutdown_logout():
    client.sendall(bytes("SHUTDOWN", "utf8"))
    sl.shutdown_logout(client, root)
    return

def mac_address():
    client.sendall(bytes("MAC", "utf8"))
    mac.mac_address(client)
    return

def directory_tree():
    return

def app_process():
    client.sendall(bytes("APP_PRO", "utf8"))
    tmp = ap.App_Process_UI(root, client)
    tmp.button_6.configure(command = lambda: back(tmp))
    return

def disconnect():
    f2.place_forget()
    f1.place(x = 0, y = 0)
    client.sendall(bytes("QUIT", "utf8"))
    return

def keylogger():
    client.sendall(bytes("KEYLOG", "utf8"))
    tmp = kl.Keylogger_UI(root, client)
    tmp.button_6.configure(command = lambda: back(tmp))
    return

def show_main_ui():
    f1.place_forget()
    global f2
    f2 = ui2.Main_UI(root)
    f2.button_1.configure(command = live_screen)
    f2.button_2.configure(command = shutdown_logout)
    f2.button_3.configure(command = mac_address)
    f2.button_4.configure(command = directory_tree)
    f2.button_5.configure(command = app_process)
    f2.button_6.configure(command = disconnect)
    f2.button_7.configure(command = keylogger)
    return
    

def connect():
    global client
    ip = f1.input.get()
    try:
        client.connect((ip, 5656))
        tk.messagebox.showinfo(message = "Connect successfully!")
        show_main_ui()
    except:
        tk.messagebox.showerror(message = "Cannot connect!")       
    return

f1.button_1.configure(command = connect)
root.mainloop()