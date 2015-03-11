"""Prints the environment variables and some Modules API output."""


import cgi
import os

from google.appengine.api import modules
from google.appengine.api import users
import webapp2


PAGE_TEMPLATE = """\
<html>
  <head>
    <title>printenv</title>
  </head>
  <body>
  <a href="{}">login</a><br><a href="{}">logout</a>
  <h1>The environment variables are:</h1>
  {}
  <h1>The CGI arguments are:</h1>
  {}
  <h1>The Modules API results are:</h1>
  {}
  </body>
</html>
"""
KEY_VALUE_TEMPLATE = '<b><tt>{}</tt></b> = <tt>{}</tt>'
STDIN_TEMPLATE = ('No CGI arguments given; here are the contents '
                  'of stdin (length={}):')


def html_for_env_var(key):
    """Returns an HTML snippet for an environment variable.

    Args:
        key: A string representing an environment variable name.

    Returns:
        String HTML representing the value and variable.
    """
    value = os.getenv(key)
    return KEY_VALUE_TEMPLATE.format(key, value)


def html_for_cgi_argument(argument, form):
    """Returns an HTML snippet for a CGI argument.

    Args:
        argument: A string representing an CGI argument name in a form.
        form: A CGI FieldStorage object.

    Returns:
        String HTML representing the CGI value and variable.
    """
    value = form[argument].value if argument in form else None
    return KEY_VALUE_TEMPLATE.format(argument, value)


def html_for_modules_method(method_name, *args, **kwargs):
    """Returns an HTML snippet for a Modules API method.

    Args:
        method_name: A string containing a Modules API method.
        args: Positional arguments to be passed to the method.
        kwargs: Keyword arguments to be passed to the method.

    Returns:
        String HTML representing the Modules API method and value.
    """
    method = getattr(modules, method_name)
    value = method(*args, **kwargs)
    return KEY_VALUE_TEMPLATE.format(method_name, value)


class MainHandler(webapp2.RequestHandler):

    def get(self):
        """GET handler that serves environment data."""
        environment_variables_output = [html_for_env_var(key)
                                        for key in sorted(os.environ)]

        cgi_arguments_output = []
        if os.getenv('CONTENT_TYPE') == 'application/x-www-form-urlencoded':
            # Note: a blank Content-type header will still sometimes
            # (in dev_appserver) show up as 'application/x-www-form-urlencoded'
            form = cgi.FieldStorage()
            if not form:
                cgi_arguments_output.append('No CGI arguments given...')
            else:
                for cgi_argument in form:
                    cgi_arguments_output.append(
                            html_for_cgi_argument(cgi_argument, form))
        else:
            data = ''
            cgi_arguments_output.append(STDIN_TEMPLATE.format(len(data)))
            cgi_arguments_output.append(cgi.escape(data))

        modules_api_output = [
            html_for_modules_method('get_current_module_name'),
            html_for_modules_method('get_current_version_name'),
            html_for_modules_method('get_current_instance_id'),
            html_for_modules_method('get_modules'),
            html_for_modules_method('get_versions'),
            html_for_modules_method('get_default_version'),
            html_for_modules_method('get_hostname'),
        ]

        result = PAGE_TEMPLATE.format(
            users.CreateLoginURL(self.request.url),
            users.CreateLogoutURL(self.request.url),
            '<br>\n'.join(environment_variables_output),
            '<br>\n'.join(cgi_arguments_output),
            '<br>\n'.join(modules_api_output),
        )

        self.response.write(result)
    post = get

APP = webapp2.WSGIApplication([
    ('/work/.*', MainHandler)
], debug=True)
