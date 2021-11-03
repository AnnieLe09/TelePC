import tkinter as tk
import socket, pickle
import os

BUFSIZ = 1024 * 4
SEPARATOR = "<SEPARATOR>"

def recvall(sock): 
    data = b''
    while True:
        while True:
            try:
                part = sock.recv(BUFSIZ)
                data += part
                if len(part) < BUFSIZ:
                    break
            except socket.error:
                return
        if data:
            break
    return data

def sendListDirs(sock):
    path = sock.recv(BUFSIZ).decode()
    if not os.path.isdir(path):
        return [False, path]

    file_name = "dirs.pkl"
    try:
        open_file = open(file_name, "wb")
        pickle.dump(os.listdir(path), open_file)
        open_file.close()
        with open(file_name, "rb") as f:
            while True:
                bytes_read = f.read(BUFSIZ)
                if not bytes_read:
                    break
                sock.sendall(bytes_read)
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
def copyFile(sock):
    received = sock.recv(BUFSIZ).decode()
    filename, path = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    sock.sendall("received filename".encode())
    data = recvall(sock)
    with open(path + filename, "wb") as f:
        f.write(data)
    sock.sendall("received content".encode())

# copy file from server to client
def copyFileTo(sock):
    sock.sendall("OK".encode())
    filename = sock.recv(BUFSIZ).decode()
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
            copyFile(client)
            isMod = False

        # copy file from server to client
        elif (mod == "COPY"):
            client.sendall("OK".encode())
            copyFileTo(client)
            isMod = False

        elif (mod == "DEL"):
            client.sendall("OK".encode())
            delFile(client)
            isMod = False

        else:
            return