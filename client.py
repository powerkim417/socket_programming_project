from socket import *
from threading import Thread
from tkinter import *

def recv_msg(client_sock):
    global text
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        text.insert('insert',data.decode())
        text.insert('insert','\n')

def send_msg(event):
    global client_sock
    global entry
    client_sock.send(entry.get().encode())

def terminate_chatbox(event):
    chat.destroy()

try:
    host_ip = input('Server IP: ')
    client_sock = socket(AF_INET, SOCK_STREAM) 
    client_sock.connect((host_ip, 8080))

    chat = Tk()
    chat.title('Chatbox_NetworkProject')
    chat.geometry('390x510+500-100')
    chat.resizable(1,1)
        
    text=Text(chat)
    text.pack()

    frame=Frame(chat)
    frame.pack()

    mes = Label(frame,text="Message")
    mes.pack(side='left')
    entry = Entry(frame, width = 40)
    entry.pack(side='left')

    thd = Thread(target=recv_msg, args=(client_sock,))
    thd.daemon = True
    thd.start()

    #send button
    #<Button-1> is left mouse click.   
    button = Button(frame,text ='Send')
    button.pack()
    button.bind('<Button-1>',send_msg)

    exit_frame=Frame(chat)
    exit_frame.pack()

    button = Button(exit_frame,text ='Exit')
    button.pack()
    button.bind('<Button-1>',terminate_chatbox)
    #repeat until exit
    chat.mainloop()    

    client_sock.close() 

except ConnectionRefusedError:
    print('*** Server is not ON, Try again. ***')
