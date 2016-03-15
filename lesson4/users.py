import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape=True)



class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self,template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		visits = self.request.cookies.get('visits','0')
		# make sure visits is an int
		if visits.isdigit():
			visits = int(visits) + 1
		else:
			visits = 0
		self.response.headers.add_header('Set-Cookie', 'visits=%s'%visits)

		if visits > 100:
			self.write('You are the best ever!')
		else:
			self.write("You've been here %s times!" % visits)


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)

