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
    s.settimeout(1)

    try:
        con = s.connect((str(targethost),int(scanport)))

        with print_lock:
            ScanResults.append(targethost)
            print("open Port: "+scanport+" on Host: "+str(targethost))
        con.close()
    except:
        pass


def start(network=None,port=None):
    global target
    global scanport
 
        
        
    print("##############################################")
    print("# IPWORXS Port Sweep  Scanner                        #")
    print("##############################################")
    print("# Scans a given Network for SMB Ports        #")
    print("")

    if network is None:
        target= input("Please enter a Network to Scan (in CIDR Format for example 192.168.1.0/24): ")
        ipifa = ipaddress.ip_network(target)
    else:
        ipifa = ipaddress.ip_network(network)
    
    if port is None:
        scanport = input("Please enter a Port to Scan: ")
    else:
        scanport = port

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
    for worker in ipifa.hosts():
        q.put(worker)
   
    q.join()

    print("")
    print("Duration: "+str(datetime.datetime.now() - begin_time))
    print("found Hosts with open  Ports: "+scanport+" on Host: "+str(len(ScanResults)))
    print("")
    print("Sorted List:")
    print(sorted(ScanResults))
  

def threader():
    while True:
        worker = q.get()
        SmbScan((worker))
        q.task_done()


if __name__ == "__main__":
    network = sys.argv[1] if len(sys.argv) > 1 else None
    port = sys.argv[2] if len(sys.argv) > 1 else None
    start(network, port)