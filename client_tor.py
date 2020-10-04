
from stem import Signal
from stem import CircStatus
from stem.control import Controller
import threading
import os
import urllib2
headers ={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0', 'Accept-Encoding' : 'gzip, deflate', 'Accept' :'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
timeout_time_url = 200
timeout_time_thread= 100
url = "http://example.com/file.jpg"
def new_identity():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        for circ in controller.get_circuits():
            if circ.status != CircStatus.BUILT:continue
            entry_fingerprint = circ.path[0][0]
            entry_descriptor = controller.get_network_status(entry_fingerprint, None)

            if entry_descriptor:
                print "Circuit %s starts with %s" % (circ.id, entry_descriptor.address)


def save_file(url):
    try:
        request = urllib2.Request(url, headers=headers)
        raw_data = urllib2.urlopen(request, timeout=timeout_time_url)
        with open(os.path.basename(url), "wb") as f:
            f.write(raw_data.read())
    except Exception,e: 
        print str(e)
        
def main(url, timeout_time_thread):
    new_identity()
    save_file(url)

thread = threading.Thread(target = main,args = (url, timeout_time_thread) )
thread.start()
thread.join(timeout_time_thread)
if thread.is_alive():
    main.terminate()
    thread.join()
    
    
    
    