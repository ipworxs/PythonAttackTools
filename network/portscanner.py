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
    s.settimeout(100)
    try:
        print(port, end =" ")
        con = s.connect((target,port))
        with print_lock:
            ScanResults.append(port)
        con.close()
    except:
        pass


def start(host=None):

    global target
    target = host
    
    # Create the queue and threader 
    begin_time = datetime.datetime.now()

    global q
    q = Queue()

    # how many threads are we going to allow for
    for x in range(500):
        t = threading.Thread(target=threader)
  
        # classifying as a daemon, so they will die when the main dies
        t.daemon = True

        # begins, must come after daemon definition
        t.start()


    start = time.time()

    # 100 jobs assigned.
    for worker in range(1,65535):
        q.put(worker)

    # wait until the thread terminates.
   

    q.join()
    print("Duration: "+str(datetime.datetime.now() - begin_time))
    print(sorted(ScanResults))
  


# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()

        # Run the example job with the avail worker in queue (thread)
        portscan(worker)

        # completed with the job
        q.task_done()


if __name__ == "__main__":
    a = str(sys.argv[1])
    start(a)