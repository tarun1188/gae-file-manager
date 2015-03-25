import base64
from services.helper import Helper

__author__ = 'Tarun'

import urllib
import json
import hashlib
from google.appengine.api import images
from handlers import BaseHandler
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import logging
from models.models import Directory, File, User
from services.response_renderer import ComplexEncoder

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class FileHandler(BaseHandler):
    def get_upload_url(self):
        if not self.request.authorization:
            self.response.status = 401
            self.response.headers['WWW-Authenticate'] = 'Basic realm="GAE File Manager"'
            self.render_json(dict(msg="Unauthorized request"))
            return
        else:
            user_header = base64.decodestring(self.request.authorization[1])
            user_id = user_header[0:user_header.find(":")]
            password = user_header[user_header.find(":")+1:]
            log.info(user_id)
            log.info(password)
            md5_generator = hashlib.md5()
            md5_generator.update(password)
            if not Helper.fetch_entity(User, user_id=user_id, password=md5_generator.hexdigest()):
                self.response.status = 401
                self.response.headers['WWW-Authenticate'] = 'Basic realm="GAE File Manager"'
                self.render_json(dict(msg="Unauthorized request"))
                return

            count = self.request.get("count")
            count = 1 if not count else int(count)
            blob_urls = []
            for x in range(count):
                upload_url = blobstore.create_upload_url('/upload')
                blob_urls.append(upload_url)
            log.debug(blob_urls)
            self.render_json(dict(blob_urls=blob_urls))


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        # index = self.request.get("index")
        # offset = self.request.get("offset")
        save_file = True if self.request.get("dl") == "1" else None
        # index = 0 if not index else int(index)
        # offset = 500 if not offset else int(offset)
        # resource = str(urllib.unquote(resource))
        try:
            resource = int(resource)
        except Exception:
            pass
        file_ = File.get_by_id(resource)
        if file_:
            blob_info = blobstore.BlobInfo.get(file_.blob)
            self.send_blob(blob_info, save_as=save_file) if save_file else \
                self.send_blob(blob_info)
        else:
            self.response.status = 404
            self.response.write("File not found")


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        file_path = urllib.unquote_plus(self.request.get("path"))
        blob_info = upload_files[0]
        if not file_path:
            blobstore.delete(blob_info.key())
            self.response.status = 400
            response_dict = dict(msg='Missing parameter "path"')
        else:
            paths = file_path.split("/")
            for index, name in enumerate(paths):
                if name:
                    path = "/" if paths[index-1] == "" else file_path[0:file_path.index(name)-1]
                    dir_ = Directory.query(Directory.path == path, Directory.name == name).fetch()
                    if not dir_:
                        dir_ = Directory()
                        dir_.name = name
                        dir_.path = path
                        dir_.put()
            file_ = File()
            file_.blob = blob_info.key()
            file_.path = file_path
            file_.description = self.request.get("description")
            file_.put()
            response_dict = dict(file_name=blob_info.filename, size=blob_info.size,
                                 file_type=blob_info.content_type,
                                 file_url="https://gae-file-manager.appspot.com/serve/"+str(file_.key.id()))
            if "image" in blob_info.content_type:
                response_dict["image_url"] = images.get_serving_url(blob_info.key())
        rv = json.dumps(response_dict, cls=ComplexEncoder)
        self.response.write(rv)