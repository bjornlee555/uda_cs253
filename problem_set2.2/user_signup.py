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
						<input type="text" name="username" value="%(username)s" required>
					</td>
					
					<td class="error">
						<div >%(error_1)s</div>
					</td>
				</tr>
				<tr>
					<td class="label">
						Password
					</td>
					<td>
						<input type="text" name="password" value="%(password)s" required>
					</td>
					<td class="error">
						<div >%(error_2)s</div>
					</td>
				</tr>
				<tr>
					<td class="label">
						Verify Password
					</td>
					<td>
						<input type="text" name="verify" value="%(verify)s" required>
					</td>
					<td class="error">
						<div >%(error_3)s</div>
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
						<div >%(error_4)s</div>
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

class MainPage(webapp2.RequestHandler):

	def write_form(self, error_1="", error_2="", error_3="", error_4="", 
					username="", password="",verify="",email=""):
		self.response.out.write(form % {"error_1": error_1, "error_2": error_2, 
										"error_3": error_3, "error_4": error_4, 
										"username":escape_html(username), 
										"password":escape_html(password), 
										"verify":escape_html(verify), 
										"email":escape_html(email)})

	def get(self):
		self.write_form()
		#self.response.write(form)

	def post(self):
		a_username = self.request.get('username')
		a_password = self.request.get('password')
		a_verify = self.request.get('verify')
		a_email = self.request.get('email')

		username = valid_username(a_username)
		password = valid_password(a_password)
		verify=valid_password(a_verify)
		email = valid_email(a_email)

		if username and password and a_password==a_verify:
			self.redirect("/welcome")

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Welcome, ")



app = webapp2.WSGIApplication([
    ('/', MainPage), ('/welcome', WelcomeHandler)], debug=True)
