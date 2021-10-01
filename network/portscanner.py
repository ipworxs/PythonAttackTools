import threading
from queue import Queue
import time
import socket
import sys
import datetime


# Thread Lock
print_lock = threading.Lock()

ScanResults = []

# Port Scan function, which collect the results.
def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)

    try:
        con = s.connect((target,port))
        with print_lock:
            ScanResults.append(port)
            print("open TCP Port:"+str(port))
        con.close()
    except:
        pass


def start(host=None):
    global target

   
    
    print("##############################################")
    print("# IPWORXS Port Scanner                       #")
    print("##############################################")
    print("# Scans a given Host for full TCP Port Range #")
    print("")

    if host is None:
        target= input("Please enter a Host to Scan: ")
    else:
         target = host


    # Begin Timer
    begin_time = datetime.datetime.now()

    global q
    q = Queue()

    # Define Threads count
    for x in range(2500):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()


    start = time.time()

    # 100 jobs assigned.
    for worker in range(1,65535):
        q.put(worker)
   
    q.join()

    print("")
    print("Duration: "+str(datetime.datetime.now() - begin_time))
    print("found openports: "+str(len(ScanResults)))
    print("")
    print("Sorted List:")
    print(sorted(ScanResults))
  

def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else None
    start(a)