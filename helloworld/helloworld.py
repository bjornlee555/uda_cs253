import webapp2
import cgi

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
		<form method = "post">
			What is your birthday?
			<br>
			<table>
				<tr>
					<td class="label"> 
						Month
					</td>
					<td>
						<input type="text" name="month" value="%(month)s">
					</td>

				</tr>

				<tr>
					<td class="label">  
						Day
					</td>
					<td>
						<input type="text" name="day" value="%(day)s">
					</td>
					<td class="error">
						<div>%(error_a)s</div>
					</td>
				</tr>

				<tr>
					<td class="label">  
						Year
					</td>
					<td>
						<input type="text" name="year" value="%(year)s">
					</td>
				</tr>
			</table>

			<div style="color: red">%(error)s</div>

			<br>
			<br>
			<input type="submit">

		</form>
	</body>

</html>

"""



months = ['January','February','March','April','May','June','July','August','September','October','November','December']

def valid_year(year):
	if year and year.isdigit() and int(year) in range(1900, 2021):
	    return int(year)

def valid_day(day):
	if day and day.isdigit():
	    day = int(day)
	    if day > 0 and day <=31:
	        return day
          
def valid_month(month):
	if month != "":
	    month = month.capitalize()
	    if month in months:
	        return month
	else:
	    return None

def escape_html(s):
	return cgi.escape(s, quote = True)

class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", error_a="",month="", day="", year=""):
    	self.response.out.write(form % {"error": error,
    									"error_a": error_a,
    									"month": escape_html(month),
    									"day": escape_html(day),
    									"year": escape_html(year)})

    def get(self):
        self.write_form()
        #self.response.write(form)
	
    def post(self):
    	user_month = self.request.get('month')
    	user_day = self.request.get('day')
    	user_year = self.request.get('year')

    	month =  valid_month(user_month)
    	day =  valid_day(user_day)
    	year =  valid_year(user_year)

    	if not (month and day and year):
    		self.write_form("That doesn't look valid to me, friend.",
    						"that's a good month!",
    						user_month, user_day, user_year)
    		#self.response.out.write(form)
    	else:
			self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Thanks! That's a totally valid date!")



app = webapp2.WSGIApplication([
    ('/', MainPage), ('/thanks', ThanksHandler)], debug=True)


