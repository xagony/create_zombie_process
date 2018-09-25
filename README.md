# Create Zombie
So let's start by defining what zombie process is - a zombie (defunct) process is the process that has completed execution, but its parent process has not yet read this process's exit code. Zombie processes take up almost no system resources - only PID in the process table and 8 bytes of RAM to store its exit code and some metadata. Zombie is removed after its exit code was read by its parent. Even though zombies do not use much of system resources they can still be dangerous as they can bulk up the process table, which by default in x86_32 systems can store only 32767 processes. 

Example of python process in zombie state (Z+):
```
(env) [root@centos ~]# ps ax | grep Z
 5113 pts/0    Z+     0:00 [python] <defunct>
```
## Creating zombie
Initially, I have used the subprocess32 library ([create_zombie.py](create_zombie.py)) to create a zombie process - this lib provides a high-level interface to the python’s os library. It did its job, however the flipside of being high-level is that it does hide some internals. So I have made a decision to implement the same functionality using **os** library.

Before diving into the code, I would like to go through some theory. In Linux, when a process spawns another process, the caller invokes the **fork()** system call to duplicate itself in memory and both processes continue execution from the same location. The new process is referred to as the child process and the calling process is referred to as the parent process. In the child process the fork() call returns 0 and in the parent process the same fork() call returns the PID of the child process. The child process is the exact copy of the parent process except PID, PPID (Parent PID) and some other properties such as process clocks and timers. After the child process finished execution by either reaching the end of the programm or encountering an exception, the exit code is returned and the process state is changed to defunct. Now is the turn of the parent process to reap the child by reading its exit code and until this happens the child remains zombie.
## Code
The [code](create_zombie_os.py) that creates a zombie process is fairly simple and consists out of 3 main logical steps:
1. Fork the existing process
2. Execute some code as a child process
3. Read child process exit code by the parent

The python os.fork() function does not directly invoke the fork() the system call. In fact python cannot natively invoke system calls so it uses C libraries to achieve this functionality. 

The first step is achieved by calling the os.fork() function, which creates a child process and returns pid value, which is assigned to the pid variable:
```
pid = os.fork()
```
So now we have 2 separate processes executing the same code. The **pid** var value in the child process is 0 and in the parent process it is /child_pid/.  
All the code after the os.fork() statement gets executed twice, however by knowing that pid of the child is 0, we can now control **what** code gets executed in **what** process:
```
if pid == 0:
  sys.exit(0)
else:
  time.sleep(60)
  os.wait()
```
The child process executes only the first part of the statement, and the parent executes only the second. 

The second step is achieved by running some code as a child. The exact code is not important, so  sys.exit(0) is a good placeholder. 

The third step is more interesting. As mentioned earlier, the code after the **else:** gets executed only by the parent process. These two processes are executed in parallel, so in order the child to remain zombie for 60 sec, a time.sleep() function is introduced to pause code execution of the parent process for 60sec.  
In order for the parent process to reap the child process, wait() system call is invoked. The python wrapper for this call is os.wait() function, which tries to read exit codes of all children.
After there is nothing else to execute, the parent reaches its end and returns the exit code, which is read by its parent - bash process:  

```
(env) [root@centos-master ~]# pstree -a
  ├─sshd -D
  │   ├─sshd
  │   │   └─bash
  │   │       └─python ./create_zombie_os.py
  │   │           └─python ./create_zombie_os.py
...
