#!/usr/bin/env python
import os, sys, time

ttl=60

pid = os.fork()

if pid == 0:
  time.sleep(ttl)
  sys.exit(0)
else:
  os.wait() 
    

  





