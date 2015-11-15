import os
import json
from tornado import web
from tornado import gen


class BaseHandler(web.RequestHandler):
    """Base class for RequestHandler objects"""

    @property
    def db(self):
        return self.application.db


class APIHandler(BaseHandler):
    """Base class for all REST api handlers"""

    def prepare(self):
        """Convert request data into a dict for easy access"""
        if self.request.body:
            try:
                data = json.loads(self.request.body)
                for key in data:
                    self.request.arguments[key] = str(key[data])
            except:
                pass

    def write_error(self, status, **kwargs):
        """Helper function for returning an error message as json"""

        if 'exc_info' in kwargs:
            _, exception, _ = kwargs['exc_info']
            msg = str(exception)
        else:
            msg = 'Unknown error.'

        self.write(json.dumps({'error': msg}))
        self.finish()
