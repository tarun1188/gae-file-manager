import logging
import urllib
from base import BaseHandler
from google.appengine.ext import blobstore
from models.models import File, Directory
__author__ = 'Tarun'

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class MainHandler(BaseHandler):

    def __init__(self, request, response):
        super(MainHandler, self).__init__(request, response)

    def get_base_url(self, params=None):
        file_path = "/" if not params else "/"+str(params)
        files_list = File.query(File.path == file_path).fetch()
        files = []
        for file_ in files_list:
            blob = blobstore.BlobInfo.get(file_.blob)
            files.append(dict(filename=blob.filename,
                              size=str((blob.size/1024)/1024) + " MB"
                              if (blob.size/1024)/1024 > 1 else str(blob.size/1024) + " KB",
                              date_added=blob.creation, url="/serve/"+str(file_.key.id()),
                              description="" if not file_.description else urllib.unquote_plus(file_.description)))
        directories = Directory.query(Directory.path == file_path).fetch()
        directory_list = []
        for dir_ in directories:
            directory_list.append(dict(name=dir_.name, path=urllib.quote(dir_.name) if
            dir_.path == "/" else urllib.quote(dir_.path+"/"+dir_.name), date_added=dir_.date_added))

        template_values = {
            'files': files,
            'directories': directory_list
        }
        self.render_html("html/file_upload.html", template_values)

    def login_user(self):
        self.render_html("html/login.html")

    def authenticate_user(self):
        email_id=  self.request.get("email_id")
        password = self.request.get("password")
        remember_me = self.request.get("remember_me")
        self.redirect("/")
