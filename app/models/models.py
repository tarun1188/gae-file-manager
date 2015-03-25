from google.appengine.ext import ndb

__author__ = 'Tarun'


class File(ndb.Model):
    path = ndb.StringProperty(required=True)
    blob = ndb.BlobKeyProperty()
    description = ndb.TextProperty()
    date_added = ndb.DateTimeProperty(auto_now_add=True)


class Directory(ndb.Model):
    path = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    date_added = ndb.DateTimeProperty(auto_now_add=True)


class User(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    is_deleted = ndb.BooleanProperty(default=False, required=True)
    # hash_key = ndb.StringProperty(required=True)