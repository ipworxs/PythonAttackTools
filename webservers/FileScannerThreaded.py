import threading
from queue import Queue
import time
import sys
import datetime
import ipaddress
import requests

# Ignore SSL Warnings
requests.packages.urllib3.disable_warnings()

# Thread Lock
print_lock = threading.Lock()

ScanResults = []



# Scan WebServer for File
def WebServerScanner(targethost):
 
    url = "http://"+str(targethost)+"/"+str(searchfile)

    a = ""
    print(url)

    try:
        r = requests.get(url, verify=False, timeout=10)
        if r.status_code == 200:
            print(url+" found")
        
            with print_lock:
                ScanResults.append(url)

                # Download if Content exist 
                open('C:\\Temp\\'+str(targethost)+"_"+str(searchfile), 'wb').write(r.content)
   

    except requests.ConnectionError:
            #do something
            a = a
      
    except requests.HTTPError:
            a = a
    
    except requests.RequetsException:
            a = a
     
    except requests.ReadTimeout:
            a = a
   
    except requests.Timeout:
            a = a
  
    except requests.ConnectTimeout:
            a = a
        
    except:
            pass
 
    finally:
            a = a


def start(network=None,filename=None):
    global target
    global searchfile
 
        
        
    print("#########################################################")
    print("# IPWORXS WebServer File Scanner & Downloader           #")
    print("#########################################################")
    print("# Scans a given Network for given Files on Webservers   #")
    print("# Downloads Content to C:\Temp (folder need to exist)   #")
    print("")

    if network is None:
        target= input("Please enter a Network to Scan (in CIDR Format for example 192.168.1.0/24): ")
        ipifa = ipaddress.ip_network(target)
    else:
        ipifa = ipaddress.ip_network(network)
    
    if filename is None:
        searchfile= input("Please enter a filename to search for: ")

    else:
        searchfile = filename


    # Begin Timer
    begin_time = datetime.datetime.now()

    global q
    q = Queue()

    # Define Threads count
    for x in range(50):
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
    print("found Hosts with open SMB Ports on Host: "+str(len(ScanResults)))
    print("")
    print("Sorted List:")
    print(sorted(ScanResults))
  

def threader():
    while True:
        worker = q.get()
        WebServerScanner((worker))
        q.task_done()


if __name__ == "__main__":
    network = sys.argv[1] if len(sys.argv) > 1 else None
    filename = sys.argv[2] if len(sys.argv) > 1 else None
    start(network, filename)