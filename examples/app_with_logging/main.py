import webapp2
from helloworld import Hello

app = webapp2.WSGIApplication([('/', Hello)], debug=True)
        
