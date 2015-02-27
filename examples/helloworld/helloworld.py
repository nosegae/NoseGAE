import webapp2
from jinja2 import Environment


class Hello(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        env = Environment()
        template = env.from_string("Hello {{ greeting }}!")
        self.response.out.write(template.render(greeting='world'))

app = webapp2.WSGIApplication([('/', Hello)], debug=True)