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

How to test multithreading and the lock:
    1. Do 2 simultaneous GET requests to the server. 
    2. The first request that gets the lock will receive <html><body><h1>hi!</h1></body></html>
    3. While the other request thats waiting for the lock, you will see from the python console 
        `Lock still in use <ip address of client> is waiting..`

Usage::
    python ./webserver.py [<port>]

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


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        while(global_locker.acquire(0) == False):
            sleep(1) #i added a sleep 1 second here so it doesnt get too spammy
            print "Lock still in use", self.client_address[0], "is waiting.." 

        self.wfile.write("<html><body><h1>hi!</h1></body></html>")
        sleep(15) #pretend there's a 15 second long operation on going

        global_locker.release()

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
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
