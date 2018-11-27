#!/usr/bin/env python
import os
import jinja2
import webapp2
from upload_helper import upload_file_helper


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("main.html")


class UploadFileHandler(BaseHandler):
    def post(self):
        if self.request.get('uploaded-file'):
            uploaded_file = self.request.POST.get('uploaded-file')

            url = upload_file_helper(uploaded_file=uploaded_file)

            return self.render_template("upload_success.html", params={"url": url})
        else:
            return self.error(400)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/upload', UploadFileHandler),
], debug=True)
