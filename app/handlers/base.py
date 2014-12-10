__author__ = 'Tarun'

import webapp2
from services.response_renderer import ResponseRenderer


class BaseHandler(webapp2.RequestHandler, ResponseRenderer):
    def __init__(self, request, response):
        self.initialize(request, response)