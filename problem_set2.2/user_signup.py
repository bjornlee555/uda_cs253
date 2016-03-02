import webapp2
import cgi

form = """
<!DOCTYPE html>

<html>
	<head>
		<title>User Signup</title>
		<style type="text/css">
			.label {text-align: right}
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
						<input type="text" name="username">
					</td>
				</tr>
				<tr>
					<td class="label">
						Password
					</td>
					<td>
						<input type="text" name="password">
					</td>
				</tr>
				<tr>
					<td class="label">
						Verify Password
					</td>
					<td>
						<input type="text" name="verify">
					</td>
				</tr>

				<tr>
					<td class="label">
						Email (optional)
					</td>
					<td>
						<input type="text" name="email">
					</td>
				</tr>
							
			</table>
			<input type="submit">

		</form>

	</body>

</html>

"""

class MainPage(webapp2.RequestHandler):

	def get(self):
		self.response.write(form)


app = webapp2.WSGIApplication([
    ('/', MainPage)], debug=True)
