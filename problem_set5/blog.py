import os
import webapp2
import jinja2
import re
import json
import hashlib
import hmac
import random
import string

SECRET = 'imsosecret'

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape=True)

def escape_html(s):
	return cgi.escape(s, quote = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

def valid_username(username):
	return USER_RE.match(username)

PW_RE = re.compile("^.{3,20}$")

def valid_password(password):
	return PW_RE.match(password)

EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")

def valid_email(email):
	return EMAIL_RE.match(email)

#below are 3 functions for hashing passwords
def hash_str(s):
	return hmac.new(SECRET,s).hexdigest()

def make_secure_val(s):
	return '%s|%s' % (s,  hash_str(s))

def check_secure_val(h):
	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val
	else:
		return None

def make_salt():
    return ''.join(random.sample((string.letters),5))

class Users(db.Model):
	username = db.StringProperty(required= True)
	password = db.StringProperty(required = True)
	#verify = db.StringProperty(required = True)
	email = db.StringProperty
	created = db.DateTimeProperty(auto_now_add=True)

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


class PermaHandler(Handler):

	def get(self,some_id):
		a=Blog.get_by_id(int(some_id))
		self.render("permalink.html", subject=a.subject, content=a.content, created=a.created, id=a.key().id())

# TODO: need to refactor JsonHandlers for main page and also permalink pages
class JsonHandler(Handler):
	def render_front(self,subject="",content="",created="",error=""):
		bloghome = db.GqlQuery("SELECT * FROM Blog "
							"ORDER BY created DESC")

		l = []
		for i in bloghome:
			d = {}
			d['subject'] = i.subject
			d['content'] = i.content
			l.append(d)
		j_d = json.dumps(l)
		self.write(j_d)	

	def get(self):
		self.render_front()

class PermaJsonHandler(Handler):
	def get(self,some_id):
		a=Blog.get_by_id(int(some_id))
		post_json = []
		entry = {}
		entry['content'] = a.content
		entry['subject'] = a.subject
		post_json.append(entry)
		some_json = json.dumps(post_json)
		self.write(json.dumps(some_json))
		
		self.write(some_json)

app = webapp2.WSGIApplication([(r'/blog', BlogHandler),
								(r'/blog.json', JsonHandler),
								(r'/blog/newpost',NewPostHandler),
								(r'/blog/(\d+)',PermaHandler),
								(r'/blog/(\d+).json',PermaJsonHandler),
								], debug=True)


