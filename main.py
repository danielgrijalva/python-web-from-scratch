from wsgiref.simple_server import make_server
from app.utils import get_route
<<<<<<< HEAD
from views.dashboard import Dashboard
from views.add_product import AddProduct
from views.get_product import GetProduct
from views.delete_product import DeleteProduct
from views.edit_product import EditProduct
from views.not_found import NotFound

urls = [
    (r'^$', Dashboard),
    (r'add/$', AddProduct),
    (r'product/?$', GetProduct),
    (r'delete/?$', DeleteProduct),
    (r'edit/?$', EditProduct),
=======
from app.views import index, not_found, add_product, get_product, delete_product, edit_product

urls = [
    (r'^$', index),
    (r'add/$', add_product),
    (r'product/?$', get_product),
    (r'delete/?$', delete_product),
    (r'edit/?$', edit_product),
>>>>>>> 70f9785f5985dc95068090c1b8bd2af7ec85a43c
]

def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    
    callback = get_route(path, urls)
    if callback:
        return callback(environ, start_response).serve()
    else:
        return NotFound(environ, start_response).serve()

if __name__ == '__main__':
    host = 'localhost'
    port = 8000
    server = make_server(host, port, application)
    print('Listening on http://{}:{}'.format(host, port))
    server.serve_forever()
