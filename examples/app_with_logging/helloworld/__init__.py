import webapp2
import logging

log = logging.getLogger()

class Hello(webapp2.RequestHandler):
    def get(self):
        log.info("I saw a penguin at the zoo and it told me a secret.")
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello world!')

