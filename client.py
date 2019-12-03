from socket import *
from threading import Thread

def recv_msg(client_sock):
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print(data.decode())

def client_main():
    try:

        client_sock = socket(AF_INET, SOCK_STREAM) 
        client_sock.connect(('127.0.0.1', 8080))
        thd = Thread(target=recv_msg, args=(client_sock, ))
        thd.daemon = True
        thd.start()
        
        # while msg is not exit
        # send msg to server
        # print echoed msg
        while True: 

            msg = input()
            client_sock.send(msg.encode()) 
            if msg == 'exit':
                break

        client_sock.close() 

    except ConnectionRefusedError:

        print('*** Server is not ON, Try again. ***')

client_main()
