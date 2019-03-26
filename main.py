from wsgiref.simple_server import make_server
from app.utils import get_route
from views.dashboard import Dashboard
from views.add_product import AddProduct
from views.get_product import GetProduct
from views.delete_product import DeleteProduct
from views.edit_product import EditProduct
from views.not_found import NotFound
from models.product import Product


urls = [
    (r'^$', Dashboard),
    (r'add/$', AddProduct),
    (r'product/?$', GetProduct),
    (r'delete/?$', DeleteProduct),
    (r'edit/?$', EditProduct),
]

def application(environ, start_response):
    p = Product()
    path = environ.get('PATH_INFO', '').lstrip('/')
    callback = get_route(path, urls)
    if callback:
        return callback(environ, start_response, p).serve()
    else:
        return NotFound(environ, start_response, p).serve()

if __name__ == '__main__':
    host = 'localhost'
    port = 8000
    server = make_server(host, port, application)
    print('Listening on http://{}:{}'.format(host, port))
    server.serve_forever()
