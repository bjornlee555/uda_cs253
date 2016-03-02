import webapp2
import cgi


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
					style="height: 100px; width: 400px;" >%(text)s</textarea>

			<div style="color: red">%(error)s</div>

			<br>
			<input type="submit">

		</form>
	</body>

</html>

"""

def escape_html(s):
	return cgi.escape(s, quote = True)

def rot13(a_string):
	b_string = ''
	j=''
	for i in a_string:
		j = chr(97 + (ord(i)+13)%97)
		b_string += j
	return b_string

class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", text=""):
    	self.response.out.write(form % {"error": error, 
    									"text": escape_html(text)})

    def get(self):
        
        self.write_form()
        #self.response.write(form)

    def post(self):
    	input_text = self.request.get('text')
    	self.write_form(rot13(input_text), rot13(input_text))
    	
    	#self.response.out.write(input_text)



app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)