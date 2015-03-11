"""Hello world application."""


import webapp2
from google.appengine.api import taskqueue


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, webapp2 World!')
        taskqueue.add(url='/work/do-something', params={'a': 'b'}, queue_name='awesome-stuff')


APP = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
