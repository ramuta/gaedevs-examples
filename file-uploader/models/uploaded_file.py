from google.appengine.ext import ndb


class UploadedFile(ndb.Model):
    url = ndb.StringProperty(indexed=False)
    # you can also add other fields, for example: uploader name, date created, tags etc.
