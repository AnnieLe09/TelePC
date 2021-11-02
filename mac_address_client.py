<<<<<<< HEAD
import tkinter as tk
import socket

BUFSIZ = 1024 * 4

def mac_address(client):
    client.sendall(bytes("MAC", "utf8"))
    res = client.recv(BUFSIZ).decode("utf8")
    res = res[2:].upper()
    res = '-'.join(res[i:i + 2] for i in range(0, len(res), 2))
=======
import tkinter as tk
import socket

BUFSIZ = 1024 * 4

def mac_address(client):
    client.sendall(bytes("MAC", "utf8"))
    res = client.recv(BUFSIZ).decode("utf8")
    res = res[2:].upper()
    res = '-'.join(res[i:i + 2] for i in range(0, len(res), 2))
>>>>>>> f545b813dac6a133a16b8232c4961e85e6242301
    tk.messagebox.showinfo(title='MAC Address', message=res)