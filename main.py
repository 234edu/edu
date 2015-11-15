import os
import sys
import tornado.ioloop
import tornado.web
import torndb

from edu.auth import AuthTestHandler

def main(args):
    """
        Main application entry-point.
    """

    # set up url mapping
    app = tornado.web.Application([
        (r"/test_auth", AuthTestHandler)
    ])

    # read the configuration from env vars
    app.conf = {
        'DB_HOST': os.environ.get('DB_HOST', 'localhost'),
        'DB_NAME': os.environ.get('DB_NAME', 'edu'),
        'DB_USER': os.environ.get('DB_USER', 'edu'),
        'DB_PASS': os.environ.get('DB_PASS', 'edu'),
        'DB_PORT': os.environ.get('DB_PORT')
    }

    # create the db connection
    app.db = torndb.Connection(
        host=app.conf['DB_HOST'],
        database=app.conf['DB_NAME'],
        user=app.conf['DB_USER'],
        password=app.conf['DB_PASS'])

    # start the server
    app.listen(int(os.environ.get('LISTENPORT', 8888)))
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main(sys.argv)
