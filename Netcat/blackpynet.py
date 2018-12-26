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

def client_sender:
   client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   try:
      #connect to target host
      client.connect((target,port))

      if len(buffer)
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
