import webapp2



form = """
&lt;!DOCTYPE html&gt;

&lt;html&gt;
  	&lt;head&gt;
    	&lt;title&gt;Unit 2 Rot 13&lt;/title&gt;
  	&lt;/head&gt;

  	&lt;body&gt;
    	&lt;h2&gt;Enter some text to ROT13:&lt;/h2&gt;
    	&lt;form method=&quot;post&quot;&gt;
      	&lt;textarea name=&quot;text&quot;
                	style=&quot;height: 100px; width: 400px;&quot;&gt;&lt;/textarea&gt;
      	&lt;br&gt;
      	&lt;input type=&quot;submit&quot;&gt;
    	&lt;/form&gt;
  	&lt;/body&gt;

&lt;/html&gt;
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('I am Rot13!')

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)