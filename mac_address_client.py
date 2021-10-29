import tkinter as tk
import socket

BUFSIZ = 1024 * 4

def mac_address(client):
    client.sendall(bytes("MAC", "utf8"))
    res = client.recv(BUFSIZ).decode("utf8")
    tk.messagebox.showinfo(title='MAC Address', message=res)