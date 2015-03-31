__author__ = 'Tarun'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
#This is the place where all of your URL mapping goes
route_list = [
    webapp2.Route(r'/upload-url', handler='handlers.FileHandler:get_upload_url',
                  methods="GET"),
    webapp2.Route(r'/login-user', handler='handlers.MainHandler:login_user',
                  methods="GET"),
    webapp2.Route(r'/authenticate-user', handler='handlers.MainHandler:authenticate_user',
                  methods='POST'),
    webapp2.Route(r'/create-user', handler='handlers.LoginHandler:create_user',
                  methods='POST'),
    webapp2.Route(r'/upload', handler='handlers.UploadHandler',
                  methods="POST"),
    webapp2.Route(r'/serve/<resource>', handler='handlers.ServeHandler',
                  methods="GET"),
    webapp2.Route(r'/<:.*>', handler='handlers.MainHandler:get_base_url',
                  methods="GET"),
]