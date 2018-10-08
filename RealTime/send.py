# Echo client program
import socket

HOST = 'localhost'    # The remote ho
PORT = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print('Enter "help" for command list')

while True:
    cmd = input('Enter Command: ')
    if cmd == 'help':
        print('Commands:')
        print('play')
        print('pause')
        print('add [port] [batteryCap] [batteryMaxChargeRate] [SOC] [deptime] [reqSOC]')
        print('sub [port]')
        print('modtime [port] [deptime]')
        print('modcharge [port] [reqSOC]')
        print('list')
        print('runScript [scriptFilePath]')
    s.send(cmd.encode('UTF-8'))

s.close()
print('Connection closed')