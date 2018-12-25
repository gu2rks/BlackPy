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

def usage():
   print "bLACKPY Net Tool\n\n"
   

   print "Usage: blackpypnet.py -t target_host -p port"
   print "-l --listen              - listen on [host]:[port] for ", \
         "incoming connections"
   print "-e --execute=file_to_run - execute the given file upon ", \
         "receiving a connection"
   print "-c --command             - initialize a command shell"
   print "-u --upload=destination  - upon receiving connection upload a ", \
         "file and write to [destination]\n\n"


   print "Examples:\nblackpypnet.py -t 192.168.0.1 -p 5555 -l -c\n", \
         "blackpypnet.py -t 192.168.0.1 -p 5555 -l -c\n", \
         "blackpypnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe\n", \
         "blackpypnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"\n", \
         "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
   sys.exit(0)

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
      if o in ("-h","-help"):
         usage()
      
main()
