from google.appengine.ext import webapp
import logging

log = logging.getLogger()

class Hello(webapp.RequestHandler):
    def get(self):
        log.info("I saw a penguin at the zoo and it told me a secret.")
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello world!')

def application():
    return webapp.WSGIApplication([('/', Hello)], debug=True)
