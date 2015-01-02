import sys
import webapp2


class Hello(webapp2.RequestHandler):
    def get(self):
        assert sys.modules
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello world!')

app = webapp2.WSGIApplication([('/', Hello)], debug=True)
