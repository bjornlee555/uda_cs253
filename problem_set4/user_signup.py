import webapp2
import cgi
import re

form = """
<!DOCTYPE html>

<html>
	<head>
		<title>User Signup</title>
		<style type="text/css">
			.label {text-align: right}
			.error {color:red}
		</style>
	</head>

	<body>
		<h2>Signup</h2>
		<form method="post">
			<table>
				<tr>
					<td class="label">
						Username
					</td>
					<td>
						<input type="text" name="username" value="%(username)s">
					</td>
					
					<td class="error">
						<div >%(error_a)s</div>
					</td>
				</tr>
				<tr>
					<td class="label">
						Password
					</td>
					<td>
						<input type="password" name="password" value="%(password)s">
					</td>
					<td class="error">
						<div >%(error_b)s</div>
					</td>
				</tr>
				<tr>
					<td class="label">
						Verify Password
					</td>
					<td>
						<input type="password" name="verify" value="%(verify)s">
					</td>
					<td class="error">
						<div >%(error_c)s</div>
					</td>
				</tr>

				<tr>
					<td class="label">
						Email (optional)
					</td>
					<td>
						<input type="text" name="email" value="%(email)s">
					</td>
					<td class="error">
						<div >%(error_d)s</div>
					</td>
				</tr>
							
			</table>
			<input type="submit">

		</form>

	</body>

</html>

"""

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

#the_username=""

class MainPage(webapp2.RequestHandler):

	def write_form(self,error_a="",error_b="",error_c="",error_d="",username="",password="",verify="",email=""):
		self.response.out.write(form % {"error_a":error_a,"error_b":error_b,
										"error_c":error_c,"error_d":error_d,
										"username":username,"password":password,
										"verify":verify, "email":email})

	def get(self):
		self.write_form()
		#self.response.write(form)

	def post(self):
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
			self.redirect("/welcome?username=" + username)
		elif username and password and a_password==a_verify and a_email=="":
			self.redirect("/welcome?username=" + a_username)
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
			self.write_form(error_a,error_b,error_c,error_d,username,password,verify,email)




class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		username=self.request.get("username")
		self.response.out.write("Welcome, " + username + '!')

#class BadHandler(webapp2.RequestHandler):
	#def get(self):
		#self.response.out.write("bad input :(((")



app = webapp2.WSGIApplication([
    ('/', MainPage), ('/welcome', WelcomeHandler)], debug=True)
