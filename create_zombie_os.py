#!/usr/bin/env python
import os, sys, time

ttl=60

# Fork the process
pid = os.fork()
print(pid)
if pid == 0:
 # This is the child process
 # Going zombie
  time.sleep(ttl)
  sys.exit(0)
else:
  # This is the parent process 
  # kill finished process by reading its exit code
  os.wait() 
    

  





