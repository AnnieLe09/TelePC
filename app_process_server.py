import socket, pickle, PIL.ImageGrab, psutil, struct
import os, subprocess

BUFSIZ = 1024 * 4

def send_data(client, data):
    size = struct.pack('!I', len(data))
    data = size + data
    client.sendall(data)
    return

def list_apps():
    app_name = list()
    app_id = list()
    app_threads = list()
    tmp = list()
    cmd = 'powershell "gps | Where-Object {$_.mainWindowTitle} | select Description, ID, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if not line.decode()[0].isspace():
            s = line.decode().rstrip()
            tmp.append(s)
    tmp = tmp[2:]
    for line in tmp:
        arr = line.split(" ")
        name = arr[0]
        ID = 0
        threads = arr[-1]
        # interation
        cur = 1
        for i in range (1, len(arr)):
            if len(arr[i]) != 0:
                name += ' ' + arr[i]
            else:
                cur = i + 1
                break
        for i in range (cur, len(arr)):
            if len(arr[i]) != 0:
                ID = arr[i]
                break
            
        app_name.append(name)
        app_id.append(ID)
        app_threads.append(threads)    
    return app_name, app_id, app_threads

def list_processes():
    ls1 = list()
    ls2 = list()
    ls3 = list()
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            name = proc.name()
            pid = proc.pid
            threads = proc.num_threads()
            ls1.append(str(name))
            ls2.append(str(pid))
            ls3.append(str(threads))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return ls1, ls2, ls3

def kill(pid):
    cmd = 'taskkill.exe /F /PID ' + str(pid)
    try:
        a = os.system(cmd)
        if a == 0:
            return 1
        else:
            return 0
    except:
        return 0
    
def start(name):
    os.system(name)
    return

def app_process(client):
    global msg
    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        if "QUIT" in msg and len(msg) < 20:
            return
        res = 0
        ls1 = list()
        ls2 = list()
        ls3 = list()
        action = int(msg)
        #0-kill
        if action == 0:
            pid = client.recv(BUFSIZ).decode("utf8")
            pid = int(pid)
            try:
                res = kill(pid)
            except:
                res = 0
        #1-xem
        elif action == 1:
            try:
                status = client.recv(BUFSIZ).decode("utf8")
                if "PROCESS" in status:
                    ls1, ls2, ls3 = list_apps()
                else:
                    ls1, ls2, ls3 = list_processes()
                res = 1
            except:
                res = 0
        #2-xoa
        elif action == 2:
            res = 1
        #3 - start
        elif action == 3:
            pname = client.recv(BUFSIZ).decode("utf8")
            try:
                start(pname)
                res = 1
            except:
                res = 0
        if action != 1 and action != 3:
            client.sendall(bytes(str(res), "utf8"))
        if action == 1:
            ls1 = pickle.dumps(ls1)
            ls2 = pickle.dumps(ls2)
            ls3 = pickle.dumps(ls3)
            print(" ")
            send_data(client, ls1)
            print(" ")
            send_data(client, ls2)
            print(" ")
            send_data(client, ls3)
    return