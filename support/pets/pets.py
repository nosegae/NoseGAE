import webapp2


class Pets(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello Pets!')


app = webapp2.WSGIApplication([('/', Pets)], debug=True)
