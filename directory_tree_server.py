import tkinter as tk
import socket, pickle
import os

from directory_tree_client import BUFFER_SIZE

BUFSIZ = 1024 * 4
SEPARATOR = "<SEPARATOR>"

def showTree(sock):
    listD = []
    for c in range(ord('A'), ord('Z') + 1):
        path = chr(c) + ":\\"
        if os.path.isdir(path):
            listD.append(path)
    file_name = "dirs.pkl"
    open_file = open(file_name, "wb")
    pickle.dump(listD, open_file)
    open_file.close()
    file_size = os.path.getsize(file_name)
    sock.sendall(str(file_size).encode())
    temp = sock.recv(BUFSIZ)
    with open(file_name, "rb") as f:
        data = f.read()
        sock.sendall(data)

def sendListDirs(sock):
    path = sock.recv(BUFSIZ).decode()
    if not os.path.isdir(path):
        return [False, path]

    file_name = "dirs.pkl"
    try:
        open_file = open(file_name, "wb")
        pickle.dump(os.listdir(path), open_file)
        open_file.close()
        file_size = os.path.getsize(file_name)
        sock.sendall(str(file_size).encode())
        temp = sock.recv(BUFSIZ)
        with open(file_name, "rb") as f:
            data = f.read()
            sock.sendall(data)
        return [True, path]
    except:
        sock.sendall("error".encode())
        return [False, "error"]    

def delFile(sock):
    p = sock.recv(BUFSIZ).decode()
    if os.path.exists(p):
        try:
            os.remove(p)
            sock.sendall("ok".encode())
        except:
            sock.sendall("error".encode())
            return
    else:
        sock.sendall("error".encode())
        return

# copy file from client to server
def copyFileToServer(sock):
    received = sock.recv(BUFSIZ).decode()
    if (received == "-1"):
        sock.sendall("-1".encode())
        return
    filename, filesize, path = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    sock.sendall("received filename".encode())
    data = b""
    while len(data) < filesize:
        packet = sock.recv(999999)
        data += packet
    if (data == "-1"):
        sock.sendall("-1".encode())
        return
    try:
        with open(path + filename, "wb") as f:
            f.write(data)
        sock.sendall("received content".encode())
    except:
        sock.sendall("-1".encode())

# copy file from server to client
def copyFileToClient(sock):
    filename = sock.recv(BUFSIZ).decode()
    if filename == "-1" or not os.path.isfile(filename):
        sock.sendall("-1".encode())
        return
    filesize = os.path.getsize(filename)
    sock.sendall(str(filesize).encode())
    temp = sock.recv(BUFSIZ)
    with open(filename, "rb") as f:
        data = f.read()
        sock.sendall(data)

def directory(client):
    isMod = False
    
    while True:
        if not isMod:
            mod = client.recv(BUFSIZ).decode()

        if (mod == "SHOW"):
            client.sendall("OK".encode())
            showTree(client)
            while True:
                check = sendListDirs(client)
                if not check[0]:    
                    mod = check[1]
                    if (mod != "error"):
                        isMod = True
                        break
        
        # copy file from client to server
        elif (mod == "COPYTO"):
            client.sendall("OK".encode())
            copyFileToServer(client)
            isMod = False

        # copy file from server to client
        elif (mod == "COPY"):
            client.sendall("OK".encode())
            copyFileToClient(client)
            isMod = False

        elif (mod == "DEL"):
            client.sendall("OK".encode())
            delFile(client)
            isMod = False

        elif (mod == "QUIT"):
            return
        
        else:
            client.sendall("-1".encode())