__author__ = 'Tarun'

import urllib
import json
from google.appengine.api import images
from handlers import BaseHandler
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import logging
from models.models import Directory, File
from services.response_renderer import ComplexEncoder

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class FileHandler(BaseHandler):
    def get_upload_url(self):
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
    # Upload normal files
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        file_path = urllib.unquote_plus(self.request.get("path"))
        blob_info = upload_files[0]
        if not file_path:
            blobstore.delete(blob_info.key())
            self.response.status = 400
            response_dict = dict(msg="Missing parameter path")
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
            response_dict = dict(blob_key=str(blob_info.key()), file_name=blob_info.filename, size=blob_info.size,
                                 file_type=blob_info.content_type)
            if "image" in blob_info.content_type:
                response_dict["image_url"] = images.get_serving_url(blob_info.key())
        rv = json.dumps(response_dict, cls=ComplexEncoder)
        self.response.write(rv)