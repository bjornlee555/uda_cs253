import webapp2


form = """

<!DOCTYPE html>

<html>
	<head>
		<title>Unit 2 Rot13</title>
	</head>

	<body>
		<h2>Enter some text to ROT13</h2>

		<form method="post">

			<textarea name="text" 
					style="height: 100px; width: 400px;"></textarea>

			<br>
			<input type="submit">

		</form>
	</body>

</html>

"""


class MainPage(webapp2.RequestHandler):
    def get(self):
        
        self.response.write(form)





app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)