import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))



hidden_html="""
<input type="hidden" name="food" value="%s">
"""

item_html="<li>%s</li>"

shopping_list_html="""
<br>
<br>
<h2>Shopping List</h2>
<ul>
%s
</ul>
"""

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
		n = int(self.request.get("n"))
		self.render("fizzbuzz.html", n=n)

		# output = form_html
		# # below var used to hold all the (hidden) inputs from form_html
		# output_hidden=""

		# # get_all will get all get/ hold parameters of "food" into a list
		# items=self.request.get_all("food")

		# if items:
		# 	output_items=""
		# 	for item in items:
		# 		# used to store data in url using hidden inputs to display in form_html
		# 		output_hidden += hidden_html % item
		# 		# below var is a bunch of list elements
		# 		output_items += item_html % item

		# 	output_shopping = shopping_list_html % output_items
		# 	output += output_shopping

		# #used to store the hiddeen food values for form
		# output = output % output_hidden
		# self.write(output)

class FizzBuzzHandler(Handler):
	def get(self):
		self.render('shopping_list.html')

app = webapp2.WSGIApplication([('/', MainPage),
								('/fizzbuzz',FizzBuzzHandler),
								],
								debug=True)




