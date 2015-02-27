import webapp2
from google.appengine.api import taskqueue


class Hello(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        task = taskqueue.Task(url='/worker', params={'foo': 'bar'})
        task.add(
            # must be something other than default to trigger bug:
            queue_name='background-processing'
        )
        self.response.out.write('Hello world!')
        

class Worker(webapp2.RequestHandler):
    def post(self):
        # pretend to do work...
        pass


app = webapp2.WSGIApplication([('/', Hello)], debug=True)