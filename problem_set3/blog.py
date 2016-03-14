import os
import webapp2
import jinja2
import re

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

class Blog(db.Model):
	subject = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	created = db.DateProperty(auto_now_add=True)

	# crucial to make subjects link to permalinks 
	# https://discussions.udacity.com/t/question-about-in-embed-python-in-hw3/69922/2
	def href(self):
		return "/blog/" + str(self.key().id())

class BlogHandler(Handler):
	def render_front(self,subject="",content="", created="", error=""):
		bloghome = db.GqlQuery("SELECT * FROM Blog "
							"ORDER BY created DESC")


		self.render("blog.html", subject=subject, content=content, created=created, error=error,bloghome=bloghome)

	def get(self):
		self.render_front()

class NewPostHandler(Handler):
	def get(self):
		self.render("newpost.html")

	def post(self):
		subject=self.request.get("subject")
		content=self.request.get("content")

		if subject and content:
			a=Blog(subject=subject, content=content)
			a.put()
			a_id=a.key().id()

			# this avoid annoying browser reminder to reload the page
			self.redirect("/blog/%d" %a_id)
		else: 
			error="we both need a subject and some content!"
			self.render("newpost.html", error=error)


class BlogPermalinkHandler(Handler):

	def get(self,some_id):
		a=Blog.get_by_id(int(some_id))
		self.render("permalink.html", subject=a.subject, content=a.content, created=a.created, id=a.key().id())


app = webapp2.WSGIApplication([('/blog', BlogHandler),
								('/blog/newpost',NewPostHandler),
								('/blog/(\d+)',BlogPermalinkHandler),
								], debug=True)


