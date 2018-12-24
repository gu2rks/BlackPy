import socket

target_host = "www.facebook.com"
target_port = 80

#create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect the clinet
client.connect((target_host,target_port))

#send some data
client.send("GET / HTTP\1.1\r\nHost: facebook.com\r\n\r\n")

#recevie some data
response = client.recv(3000)

print response