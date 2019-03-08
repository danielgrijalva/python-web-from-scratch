from wsgiref.simple_server import make_server
from app.utils import get_route
from app.views import index, test, not_found

urls = [
    (r'^$', index),
    (r'test/?$', test),
]

def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    
    callback = get_route(path, urls)
    if callback:
        return callback(environ, start_response)
    else:
        return not_found(environ, start_response)

if __name__ == '__main__':
    server = make_server('localhost', 8000, application)
    server.serve_forever()
