import os
import re
import sys
import webapp2
import jinja2
import urllib2
import time
import logging

from xml.dom import minidom
from string import letters
from google.appengine.ext import db
from google.appengine.api import memcache

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape=True)



class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self,template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

GMAPS_URL = "https://maps.googleapis.com/maps/api/staticmap?size=600x300&maptype=roadmap&%r&key=AIzaSyD9KgC0eBH4Hre-6TNwUr9QqJcZrTCVyw4"

def gmaps_img(points):
    append = ''
    for p in points:
        append+='markers=%d,%d&'%(p.lat,p.lon)
    append = append[:-1]
    return GMAPS_URL % append

IP_URL = "http://ip-api.com/xml/23.24.209.241"
def get_coords():
	url = IP_URL
	content = None
	try:
		content =  urllib2.urlopen(url).read()
	except urllib2.URLError:
		return

	if content:
		d = minidom.parseString(content)
		status = d.getElementsByTagName("status")[0].childNodes[0].nodeValue
		if status == "success":
			lonNode = d.getElementsByTagName("lon")[0]
        	latNode = d.getElementsByTagName("lat")[0]
        	if lonNode and latNode and lonNode.childNodes[0].nodeValue and latNode.childNodes[0].nodeValue:
        		lon = lonNode.childNodes[0].nodeValue
            	lat = latNode.childNodes[0].nodeValue
            	return db.GeoPt(lat, lon)

class Art(db.Model):
	title = db.StringProperty(required=True)
	art=db.TextProperty(required=True)
	created=db.DateTimeProperty(auto_now_add=True)
	coords = db.GeoPtProperty()

def top_arts(update = False):
		key = 'top'
		arts = memcache.get(key)
		if arts is None or update:
			logging.error("DB QUERY")
			arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC ")

			arts = list(arts)
			memcache.set(key,arts)
		return arts

class MainPage(Handler):
	def render_front(self,title="", art="", error=""):		
		# prevent the running of multiple databse queries
		arts = top_arts()

		#find which arts have coords
		
		img_url = None
		# points = filter(None,(a.coords for a in arts))

		#my original way of solving but has linger code
		points = []
		for a in arts:
			if a.coords:
				points.append(a.coords)
		# if we have any arts coords, make an image url
		
		if points:
			img_url = gmaps_img(points)

		#display the image url

		self.render("front.html",title=title,art=art,error=error,arts=arts, img_url=img_url)


	def get(self):
		#self.write(self.request.remote_addr)
		#self.write(repr(get_coords()))
		self.render_front()

	def post(self):
		title=self.request.get("title")
		art = self.request.get("art")

		if title and art:
			a = Art(title=title, art=art)
			coords = get_coords()
			if coords:
				a.coords = coords
			a.put()
			# rerun the query and update the cache
			#top_arts(True)
			time.sleep(2)
			top_arts(True)
			time.sleep(2)

			self.redirect("/")
		else:
			error = "we need both SOME BLOODY title and some artwork!"
			self.render_front(title,art,error)


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)