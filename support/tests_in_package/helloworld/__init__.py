from google.appengine.ext import webapp

class Hello(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello world!')

def application():
    return webapp.WSGIApplication([('/', Hello)], debug=True)
