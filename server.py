import socket
import socketserver
from _thread import *

class Manager:
    def __init__(self):
        self.userlist = {}

    def add_user(self, conn, addr):
        # if already existing user
        if addr in self.userlist:
            conn.send('Already Existing Host'.encode())
            return

        self.userlist[addr] = conn

        self.broadcast('*** [{}:{}] entered. ***'.format(addr[0], addr[1]))
        print('*** Currently {} User(s) Online ***'.format(len(self.userlist)))

    def remove_user(self, addr):
        if addr not in self.userlist:
            return
    
        del self.userlist[addr]

        self.broadcast('*** [{}:{}] left. ***'.format(addr[0], addr[1]))
        print('*** Currently {} User(s) Online ***'.format(len(self.userlist)))

    def msg_handle(self, addr, msg):
        if (msg.strip() == 'exit'):
            self.remove_user(addr)
            return -1
        else:
            self.broadcast_msg(addr, msg)
            print('[{}:{}] {}'.format(addr[0], addr[1], msg))

    def broadcast(self, data): # to all clients
        for conn in self.userlist.values():
            conn.send(data.encode())

    def broadcast_msg(self, sender_addr, msg): # to all clients, but to sender: [You] asdfasdf
        for addr in self.userlist:
            if addr == sender_addr: self.userlist[addr].send('[You] {}'.format(msg).encode()) # if my msg
            else: self.userlist[addr].send('[{}:{}] {}'.format(sender_addr[0], sender_addr[1], msg).encode())

mng = Manager()

def threaded(client_sock, addr):
    print('*** [{}:{}] Connected ***'.format(addr[0], addr[1])) 
    
    
    try:
        mng.add_user(client_sock, addr)
        while True: 
            msg = client_sock.recv(1024)
            if not msg:
                print('*** [{}:{}] Disconnected ***'.format(addr[0], addr[1])) 
                break
            if mng.msg_handle(addr, msg.decode()) == -1:
                client_sock.close()
                break

    except ConnectionResetError: # Exit
        print('*** [{}:{}] Exit ***'.format(addr[0], addr[1])) 

    mng.remove_user(addr)
             
    client_sock.close() 

def server_main():
    try: 
        # Object initialization
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind
        server_sock.bind(('', 8080)) 

        # Listen
        server_sock.listen(1) 
        print('*** Server ON ***')

        # If new client connects, return new socket(for client) in accept()
        while True:
            start_new_thread(threaded, server_sock.accept())

        server_sock.close()

    except KeyboardInterrupt:

        print('*** Server OFF ***')

    except ConnectionRefusedError:
        
        print('*** ConnectionRefusedError, Try again. ***')

server_main()