import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.api import taskqueue

class Hello(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        task = taskqueue.Task(url='/worker', params={'foo': 'bar'})
        task.add(
            # must be something other than default to trigger bug:
            queue_name='background-processing'
        )
        self.response.out.write('Hello world!')
        
class Worker(webapp.RequestHandler):
    def post(self):
        # pretend to do work...
        pass

def application():
    return webapp.WSGIApplication([
        ('/', Hello),
        ('/worker', Worker)
    ], debug=True)
        
def main():
    wsgiref.handlers.CGIHandler().run(application())

if __name__ == '__main__':
    main()
