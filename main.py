from wsgiref.simple_server import make_server
from app.utils import get_route
from app.views import index, not_found, add_product, get_product, delete_product, edit_product

urls = [
    (r'^$', index),
    (r'add/$', add_product),
    (r'product/?$', get_product),
    (r'delete/?$', delete_product),
    (r'edit/?$', edit_product),
]

def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    
    callback = get_route(path, urls)
    if callback:
        return callback(environ, start_response)
    else:
        return not_found(environ, start_response)

if __name__ == '__main__':
    host = 'localhost'
    port = 8000
    server = make_server(host, port, application)
    print('Listening on http://{}:{}'.format(host, port))
    server.serve_forever()
