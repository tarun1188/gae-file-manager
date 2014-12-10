__author__ = 'Tarun'

import json
import datetime
import logging
import os
import google.appengine.ext.webapp.template as template

log = logging.getLogger(__name__)


class ResponseRenderer(object):
    """Different types of responses"""

    def __init__(self, arg):
        super(ResponseRenderer, self).__init__()

    def render_unauthorized(self):
        self.response.status = 401
        self.render_json({'response': 401})

    def render_html(self, _template, _template_values=None):
        tmpl = os.path.join(os.path.dirname(__file__), "../"+_template)
        tmpl_content = template.render(tmpl, _template_values)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(tmpl_content)

    def render_json(self, obj):
        rv = json.dumps(obj, cls=ComplexEncoder)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(rv)

    def render_text(self, obj):
        self.response.write(obj)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int((obj - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
        return None