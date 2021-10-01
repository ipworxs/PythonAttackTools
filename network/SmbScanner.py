import threading
from queue import Queue
import time
import socket
import sys
import datetime
import ipaddress

# Thread Lock
print_lock = threading.Lock()

ScanResults = []

# Port Scan function, which collect the results.
def SmbScan(targethost):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    #print(targethost)
    port = 445
    try:
        con = s.connect((targethost,port))
        with print_lock:
            ScanResults.append(targethost)
            print("open SMB Port:"+str(targethost))
        con.close()
    except:
        pass


def start(host=None):
    global target

    ipifa = ipaddress.ip_interface(host)
    print(ipifa.is_private)
    print(ipifa)
    
    print("##############################################")
    print("# IPWORXS SMB Scanner                       #")
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
    for x in range(100):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()


    start = time.time()

    # 254 jobs assigned (C Class Network)
    for worker in range(1,254):
        q.put(worker)
   
    q.join()

    print("")
    print("Duration: "+str(datetime.datetime.now() - begin_time))
    print("found Hosts with open SMB Ports: "+str(len(ScanResults)))
    print("")
    print("Sorted List:")
    print(sorted(ScanResults))
  

def threader():
    while True:
        worker = q.get()
        SmbScan("192.168.2."+str(worker))
        q.task_done()


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else None
    start(a)