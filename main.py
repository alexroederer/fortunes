#!./env/bin/python

import webapp2

MAIN_PAGE_HTML = """\
<html>
  <head>
    <title>MYSTIC COOKIE</title>
  </head>
  <body>
    <h3>THE MYSTIC COOKIE</h3>
    <p>You have discovered the deep, ominous pool of thought
    that is the font of knowledge for 
    the <a href="https://twitter.com/mystic_cookie">@MYSTIC_COOKIE</a>.
    The great and powerful cookie is a twitter bot which provides 
    startlingly accurate advice to souls in search of guidance, 
    or who just want an extremely cheap confection. 
    </p>
  </body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
    ], debug=True)

