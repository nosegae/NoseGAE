import webapp2
from google.appengine.api import users


class Hello(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()  # fails unless environ setup right
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(user.email())


app = webapp2.WSGIApplication([('/', Hello)], debug=True)
