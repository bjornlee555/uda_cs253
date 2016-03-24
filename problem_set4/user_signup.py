import webapp2
import cgi
import re
import os
import jinja2
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

class MainPage(Handler):
	def get(self):
		self.response.out.write('Hello World!')

class SignupHandler(Handler):

	# def write_form(self,error_a="",error_b="",error_c="",error_d="",username="",password="",verify="",email=""):
	# 	self.response.out.write(form % {"error_a":error_a,"error_b":error_b,
	# 									"error_c":error_c,"error_d":error_d,
	# 									"username":username,"password":password,
	# 									"verify":verify, "email":email})

	def render_blog(self,error_a="",error_b="",error_c="",error_d="",
					username="",password="",verify="",email=""):
		users = db.GqlQuery("SELECT * FROM Users")
		self.render("signup.html",error_a=error_a,error_b=error_b,
					error_c=error_c,error_d=error_d,username=username,
					password=password,verify=verify,email=email)

	def get(self):
		
		self.render_blog()
		#self.response.write(form)

	def post(self):
		#c_user = ''
		#c_user2 = self.request.cookies.get('c_user')
		user_id = ''
		user_id_str = self.request.cookies.get('user_id')

		a_username = self.request.get('username')
		a_password = self.request.get('password')
		a_verify = self.request.get('verify')
		a_email = self.request.get('email')

		#the_username = a_username

		username = valid_username(a_username)
		password = valid_password(a_password)
		verify = valid_password(a_verify)
		email = valid_email(a_email)

		outcome = ['','','','',a_username,a_password,a_verify,a_email]
		count = 0

		if username and password and a_password==a_verify and email:
			h_password = hash_str(a_password)
			a = Users(username=a_username,password=h_password,email=email)
			a.put()
			a_id= a.key().id()

			new_user_id = make_secure_val(str(a_id))

			self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' %new_user_id)
			#self.response.headers.add_header('Set-Cookie', 'c_user=%s; Path=/' %str(a_username))
			self.redirect("/welcome")

		elif username and password and a_password==a_verify and a_email=="":
			a = Users(username=a_username,password=a_password,email=email)
			a.put()
			a_id= a.key().id()

			new_user_id = make_secure_val(str(a_id))

			self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' %new_user_id)
			#self.response.headers.add_header('Set-Cookie', 'c_user=%s; Path=/' %str(a_username))
			self.redirect("/welcome")

		else:
			for (i,o) in ((username,"That's not a valid username."),
							(password,"That wasn't a valid password."),
							(verify,""),
							(email,"")):
				
				if i == None:
					outcome[count] = o
				count += 1
			if a_password != a_verify:
				outcome[2]="Your passwords didn't match."
				outcome[1]=""
				outcome[5]=""
				outcome[6]=""
			if a_email !="" and email == None:
				outcome[3]="That's not a valid email."

			new_outcome = tuple(outcome)
			#newer_outcome = new_outcome + (a_username,a_password,a_verify,a_email)
			error_a,error_b,error_c,error_d,username,password,verify,email=new_outcome
			#self.write_form(error_a,error_b,error_c,error_d,username,password,verify,email)
			self.render_blog(error_a,error_b,error_c,error_d,username,password,verify,email)

class LoginHandler(Handler):
	def render_login(self, username='', password='', error=''):
		users = db.GqlQuery("SELECT * FROM Users")
		self.render("login.html",username=username, password=password,
					error = error)

	def get(self):
		self.render_login()

	def post(self):
		l_username = self.request.get('username')
		l_password = self.request.get('password')
		users = Users.all()

		if l_username and l_password:
			users.filter('username =',l_username)
			result=users.get()
			if result:
				users.filter('password =', l_password)
				result2 = users.get()
				if result2:
					l_user = result2.key().id()
					new_user_id = make_secure_val(str(l_user))
					self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' %new_user_id)
					self.redirect('/welcome')
		
		error = 'Invalid login'
		self.render_login('','',error)
			
class LogoutHandler(Handler):
	def get(self):
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
		self.redirect('/signup')

class WelcomeHandler(Handler):
	def get(self):
		current_user_id = ((self.request.cookies.get("user_id")).split('|'))[0]
		b = Users.get_by_id(int(current_user_id))
		self.response.out.write("Welcome, " + b.username + '!')

#class BadHandler(webapp2.RequestHandler):
	#def get(self):
		#self.response.out.write("bad input :(((")



app = webapp2.WSGIApplication([('/', MainPage),
								('/signup', SignupHandler),
								('/login', LoginHandler),
								('/logout', LogoutHandler), 
								('/welcome', WelcomeHandler),
								], debug=True)


