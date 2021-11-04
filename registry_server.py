import re, winreg, json
import os

from live_screen_client import BUFSIZ

def parse_data(full_path):
    try:
        full_path = re.sub(r'/', r'\\', full_path)
        hive = re.sub(r'\\.*$', '', full_path)
        if not hive:
            raise ValueError('Invalid \'full_path\' param.')
        if len(hive) <= 4:
            if hive == 'HKLM':
                hive = 'HKEY_LOCAL_MACHINE'
            elif hive == 'HKCU':
                hive = 'HKEY_CURRENT_USER'
            elif hive == 'HKCR':
                hive = 'HKEY_CLASSES_ROOT'
            elif hive == 'HKU':
                hive = 'HKEY_USERS'
        reg_key = re.sub(r'^[A-Z_]*\\', '', full_path)
        reg_key = re.sub(r'\\[^\\]+$', '', reg_key)
        reg_value = re.sub(r'^.*\\', '', full_path)
        return hive, reg_key, reg_value
    except:
        return None, None, None

def query_value(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
        winreg.QueryValueEx(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except:
        return ["0", "0"]


def get_value(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
        value_of_value, value_type = winreg.QueryValueEx(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", value_of_value]
    except:
        return ["0", "0"]


def set_value(full_path, value, value_type='REG_SZ'):
    value_list = parse_data(full_path)
    try:
        winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1])
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
        winreg.SetValueEx(opened_key, value_list[2], 0, getattr(winreg, value_type), value)
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except:
        return ["0", "0"]


def delete_value(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
        winreg.DeleteValue(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except:
        return ["0", "0"]


def query_key(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2], 0, winreg.KEY_READ)
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except:
        return ["0", "0"]


def create_key(full_path):
    value_list = parse_data(full_path)
    try:
        winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])
        return ["1", "1"]
    except:
        return ["0", "0"]


def delete_key(full_path):
    value_list = parse_data(full_path)
    try:
        winreg.DeleteKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])
        return ["1", "1"]
    except:
        return ["0", "0"]

def registry(client):
    BUFSIZ = 32768
    while True:
        header = client.recv(BUFSIZ).decode("utf8")
        if("STOP_EDIT_REGISTRY" in header):
            break
        data_sz = int(header)
        data = b""
        while len(data) < data_sz:
            packet = client.recv(BUFSIZ)
            data += packet

        msg = json.loads(data.decode('utf8'))
        # extract elements
        ID = msg['ID']
        full_path = msg['path'] 
        name_value = msg['name_value']
        value = msg['value']
        v_type = msg['v_type']
        res = ['0','0']

        #ID==0 run file.reg
        #path is detail of file .reg
        if ID == 0:
            try:
                outout_file = os.getcwd() + '\\run.reg'
                with open(outout_file, 'w+') as f:
                    f.write(full_path)
                    f.close()
                os.system(r'regedit /s ' + os.getcwd() + '\\run.reg')
                res = ["1", "1"]
                print('file reg created')
            except:
                res = ["0", "0"]
                print('cannot create file reg')

        elif ID == 1:
            res = get_value(full_path + r'\\' + name_value)     

        elif ID == 2:
            res = set_value(full_path + r'\\' + name_value, value, v_type)       

        elif ID == 3:
            res = create_key(full_path)

        elif ID == 4:
            res = delete_key(full_path + r'\\')
        client.sendall(bytes(res[0], "utf8"))
        client.sendall(bytes(str(res[1]), "utf8"))

    return