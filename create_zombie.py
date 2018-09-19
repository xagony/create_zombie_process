#!/usr/bin/env python
from subprocess32 import Popen
import time
import psutil 
from psutil._exceptions import NoSuchProcess

ttl=1

zombie = Popen([''], shell=True)
time.sleep(1)
proc_status=psutil.Process(zombie.pid).status()
print("Process spawned. PID {}, status {} ".format(zombie.pid, proc_status))
print("Waiting {} sec".format(ttl))
time.sleep(ttl)

# kill zombie by reading proccess exit code
zombie.wait()

try:
  psutil.Process(zombie.pid).status()
except NoSuchProcess:
  print("{} proccess eliminated".format(proc_status))

