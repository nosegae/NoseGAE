print "-------------- running app code --------------------"
import sys
import socket
import bisect
import wsgiref.handlers

class App:
    def __call__(self, environ, start_response):
        # This won't work under GAE
        print "socket", socket
        here = socket.gethostbyname('localhost')
        start_response('200 OK', [('Content-type', 'text/plain')])
        return ['Hello %s' % here]

def application():
    return App()
        
def main():
    wsgiref.handlers.CGIHandler().run(application())

if __name__ == '__main__':
    main()
print "----------------------- end app code -----------------"
