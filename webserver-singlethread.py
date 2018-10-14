#!/usr/bin/env python
"""
ORIGINAL AUTHOR:
    https://gist.github.com/bradmontgomery/2219997

Very simple HTTP server in python that is multi threaded. Default port is 8001. If you want port 80, you need super user access.

This will only execute on python 2.7, if you want to adapt for python 3, you'll need to modify the `print` syntaxes only(i think, not tested)

This file, I've put sleep(15) right after `self.wfile.write("<html><body><h1>hi!</h1></body></html>")`. This is to 
simulate a kind of long process.


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
import SocketServer
from time import sleep #to simulate long operation functions

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")
        sleep(15) #pretend there's a 15 second long operation on going


    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")


def run(server_class=HTTPServer, handler_class=S, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd... at port %s' % (str(port))
    print 'use Ctrl+C to stop the server if using Ubuntu/Linux'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    import argparse
    parser = argparse.ArgumentParser(description='set Port number(default: 8001) and set thread Locking mechanism(defaut: Enabled)')
    parser.add_argument('-p','--port', dest='port', action='store', type=int, default=8001,
                        help='specify port number')
    args = parser.parse_args()    

    run(port=args.port)