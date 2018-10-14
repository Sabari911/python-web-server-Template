# python-web-server-Template

ORIGINAL AUTHOR:
    https://gist.github.com/bradmontgomery/2219997
    
Very simple HTTP server in python that is multi threaded. Default port is 8001. If you want port 80, you need super user access.
I use this template very often and decided to add multithreading capability.
This will only execute on python 2.7, if you want to adapt for python 3, you'll need to modify the `print` syntaxes only(i think, not tested)


There are 2 files in this project. webserver.py(multithreaded python webserver with lock) and webserver-singlethread.py.

I included both implementations in this project to illustrate differences between multithreading,single threading and using Locks.

## Testing
How to test singlthreading vs multithreading without Locks

    1. Multithreading test with Lock
        1. Execute ./webserver.py
        1. In terminal, type "time curl http://localhost:8001 & time curl http://localhost:8001;" without the quotation marks
            - This will execute 2 curls simultaneously
        1. First curl request will respond after 15s. Second curl request will respond after 30s, while second curl is waiting for the lock to be freed, you will see Lock still in use 127.0.0.1 is waiting.. in your python console

    1. Multithreading test without Lock
        1. Execute ./webserver.py -l
        1. In terminal, type "time curl http://localhost:8001 & time curl http://localhost:8001;" without the quotation marks
            - This will execute 2 curls simultaneously
        1. Both curl requests will end in 15s

    1. Singlethreading
        1. Execute ./webserver-singlethreaded.py
        1. In terminal, type "time curl http://localhost:8001 & time curl http://localhost:8001;" without the quotation marks
            - This will execute 2 curls simultaneously
        1. First curl request will respond after 15s. Second curl request will respond after 30s
