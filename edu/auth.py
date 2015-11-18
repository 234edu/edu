import os
import json
import functools
import concurrent.futures
from base import APIHandler

from tornado import web
from tornado import gen


# thread pool used for hashing
executor = concurrent.futures.ThreadPoolExecutor(2)

class UserAccount(object):
    def __init__(self, email, role):
        self.email = email
        self.role = role


def authenticated(method):
    """A method decorator for performing HMAC authentication
       in a RequestHandler method"""

    @gen.coroutine
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):

        import hashlib
        import base64
        import hmac

        user = None

        if 'Authorization' in self.request.headers:
            email, signature = self.request.headers['Authorization'].split(":")

            # canonicalize http headers for signing
            sigdata = "{0} {1}\n".format(self.request.method, self.request.uri)

            sigdata += "Content-Length:{0}\n".format(len(self.request.body))

            md5dig = hashlib.md5()
            if len(self.request.body) > 0:
                yield executor.submit(md5dig.update, self.request.body)

            sigdata += "Content-MD5:{0}\n".format(base64.b64encode(md5dig.digest()))

            # fetch the passkey from the database


            user = self.db.get("SELECT * FROM Users WHERE email=%s", email)
            if not user:
                self.write_error(status_code=401, exc_info="invalid email")
                self.finish()

            # now compute the header signature
            hmac_code = yield executor.submit(hmac.new, user.passkey, sigdata.encode(), hashlib.sha256)
            hmac_code = hmac_code.digest().encode("base64").rstrip("\n")

            if hmac_code != signature:
                self.write_error(status_code=401, exc_info="invalid Authorization signature")
                self.finish()
            else:
                self.current_user = email
                raise gen.Return(method(self, *args, user=UserAccount(user.email, 0)))

        else:
            raise gen.Return(method(self, *args, user=None, **kwargs))

    return wrapper


def cookie_auth(method):
    """
    Decorator for performing cookie-base authentication.
    Normally, you'd want to store the session token in a storage layer, and set an expire deadline for it.
    Maybe do this later.
    """
    pass

class AuthTestHandler(APIHandler):

    @authenticated
    def get(self, user=None):
        if None != user:
            data = {}
            for i in self.request.headers:
                data[i] = self.request.headers[i]


            self.write("Successfully authenticated as {0}\n".format(user.email))
            self.write(data)
        else:
            self.write("Not authenticated!")