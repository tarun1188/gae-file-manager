__author__ = 'Tarun'

import webapp2
from routes import route_list

application = webapp2.WSGIApplication(route_list)