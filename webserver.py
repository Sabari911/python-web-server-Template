#!/usr/bin/env python
"""
ORIGINAL AUTHOR:
    https://gist.github.com/bradmontgomery/2219997

Very simple HTTP server in python that is multi threaded. Default port is 8001. If you want port 80, you need super user access.
I use this template very often and decided to add multithreading capability as well a lock.

This will only execute on python 2.7, if you want to adapt for python 3, you'll need to modify the `print` syntaxes only(i think, not tested)

This file, I've put sleep(15) right after `self.wfile.write("<html><body><h1>hi!</h1></body></html>")`. This is to 
simulate a kind of long process so that you can see how locking works. Note that in acquire(0), the argument '0' means non blocking. If 
no argument is passed, the default would be a blocking lock.

Lastly, all examples that can be done with this template are only implemented during HTTP GET requests.

Usage::
    To get help:

    ./webserver.py -h 
    set Port number(default: 8001) and set thread Locking mechanism(defaut: Enabled)
    optional arguments:
    -h, --help            show this help message and exit
    -p PORT, --port PORT  specify port number
    -l, --disable-lockng

    example:
    python ./webserver.py -p 8002 -l
    This executes the webserver to listen to port 8002 and disable locking

Send a GET request::
    curl http://localhost:8001

Send a HEAD request::
    curl -I http://localhost:8001

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost:8001



"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from SocketServer import ThreadingMixIn
from threading import Lock
from time import sleep #to simulate long operation functions

global_locker = Lock()
is_locking_mechanism_enabled = True

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        #The Section below this line can be deleted for your use
        while(global_locker.acquire(0) == False and is_locking_mechanism_enabled):
            sleep(1) #i added a sleep 1 second here so it doesnt get too spammy
            print "Lock still in use", self.client_address[0], "is waiting.." 

        self.wfile.write("<html><body><h1>hi!</h1></body></html>")
        sleep(15) #pretend there's a 15 second long operation on going

        if is_locking_mechanism_enabled:
            global_locker.release()
        #The Section above this line can be deleted for your use


    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

class threadedServer(ThreadingMixIn,HTTPServer):
    '''
    Handle server in another thread
    '''    

def run(server_class=threadedServer, handler_class=S, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd... at port %s' % (str(port))
    print 'use Ctrl+C to stop the server if using Ubuntu/Linux'
    httpd.serve_forever()

if __name__ == "__main__":
    #The Section below this line can be deleted for your use
    import argparse    
    parser = argparse.ArgumentParser(description='set Port number(default: 8001) and set thread Locking mechanism(defaut: Enabled)')
    parser.add_argument('-p','--port', dest='port', action='store', type=int, default=8001,
                        help='specify port number')
    parser.add_argument('-l','--disable-lockng', dest='is_locking_mechanism_enabled',action='store_false', default=True)
    args = parser.parse_args()    
    is_locking_mechanism_enabled=args.is_locking_mechanism_enabled
    print "Locking mechanism is ", is_locking_mechanism_enabled
    #The Section above this line can be deleted for your use
    
    
    run(port=args.port) #remember to change the input argument if you delete the above lines.
