#!/usr/bin/env python
"""
ORIGINAL AUTHOR:
    https://gist.github.com/bradmontgomery/2219997

Very simple HTTP server in python that is multi threaded. Default port is 8001. If you want port 80, you need super user access.
I use this template very often and decided to add multithreading capability.

Usage::
    To get help:

    ./webserver.py -h 
    set Port number(default: 8001) and set thread Locking mechanism(defaut: Enabled)
    optional arguments:
    -h, --help            show this help message and exit
    -p PORT, --port PORT  specify port number

    example:
    python ./webserver.py -p 8002   

Usage::
    python ./webserver.py -p <port number>

Send a GET request::
    curl http://localhost:8001

Send a HEAD request::
    curl -I http://localhost:8001

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost:8001



"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import SocketServer
from SocketServer import ThreadingMixIn
from threading import Lock

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        query = urlparse.parse_qs(urlparse.urlparse(self.path).query)  #retrieve GET arguments from path
        self.wfile.write("<html><body><h1>hi! you did a GET request</h1>")
        self.wfile.write("<p>Your GET arguments is/are:</p>")
        self.wfile.write(str(query))
        self.wfile.write("</body></html>")



    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        length = int(self.headers.getheader('content-length'))
        query_string = "blank"
        if length > 0:
            query_string = self.rfile.read(length) 
            query_string = urlparse.parse_qs(query_string)
        self.wfile.write("<html><body><h1>"+ str(query_string) + "</h1></body></html>")


class threadedServer(ThreadingMixIn,HTTPServer):
    '''
    Handle server in another thread
    '''    

def run(server_class=threadedServer, handler_class=S, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd... at port %s' % (str(port))
    print 'use Ctrl+C to stop the server'
    httpd.serve_forever()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='set Port number(default: 8001)')
    parser.add_argument('-p','--port', dest='port', 
                        action='store', type=int, default=8001,
                        help='specify port number')
    args = parser.parse_args()        
    run(port=args.port) 
