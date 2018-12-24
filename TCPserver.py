import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#pass of ip and port that server going to listen on
server.bind((bind_ip,bind_port))

#listen max 5 clients
server.listen(5)

print "[*] Listening on %s:%d" %(bind_ip, bind_port)

#client-handling thread
def handle_client(client_socket):
    
    #print out what the client sends
    request = client_socket.recv(1024)
    print "[*] Received: %s" % request
    
    #send back a packet
    client_socket.send("Wellcome to Blackpy")
    
    client_socket.close()

#waiting for an incoming connection
while True: 
    client,addr = server.accept() #<--- contected server
    #client = client socket
    #addr = remote connection detail
    
    print "[*] Accepted connection from: %s:%d" %(addr[0],addr[1])
    
    #create a new thread object that points to our handle_client function, 
    #pass the client socket object as an argument.
    client_handler = threading.Thread(target=handle_client, args=(client,))
    #start the thread to handle the client connection
    client_handler.start()
    