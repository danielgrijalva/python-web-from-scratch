from .utils import read_html, get_response_data, redirect
from cgi import parse_qs, escape, FieldStorage
from .models import Model
from .template import Templite


Product = Model('crud', 'product')

def index(environ, start_response, alerts=None):
    products = Product.select_all()
    if products:
        html = Templite(read_html('dashboard'), {'products': products, 'alerts': alerts}).render()
        status, response_headers = get_response_data(html)
        start_response(status, response_headers)

        return [html.encode('utf-8')]
    else:
        status, response_headers = redirect('/add/')
        start_response(status, response_headers)    

        return ['1'.encode('utf-8')]


def add_product(environ, start_response):
    html = read_html('add_product')
    post_html = Templite(html).render({'alerts': None})

    if environ['REQUEST_METHOD'] == 'POST':
        form = dict(FieldStorage(fp=environ['wsgi.input'], environ=environ))
        
        name = form['name'].value
        description = form['description'].value
        price = form['price'].value
        stock = form['stock'].value

        data = {
            'name': form['name'].value,
            'description': form['description'].value,
            'price': form['price'].value,
            'stock': form['stock'].value,
        }

        try:
            inserted_id = Product.insert(data)
            alerts = [{
                    'context': 'success', 
                    'message': '<a href="/product?id={id}">Product #{id}</a> added.'.format(id=inserted_id)
                }]
            post_html = Templite(html, {'alerts': alerts}).render()
        except Exception as e:
            print(e)

    status, response_headers = get_response_data(post_html)
    start_response(status, response_headers)

    return [post_html.encode('utf-8')]

def get_product(environ, start_response):    
    product_id = parse_qs(environ['QUERY_STRING'])['id'][0]
    product = Product.select_one(product_id)
    html = Templite(read_html('product'), {'product': product}).render()

    status, response_headers = get_response_data(html)
    start_response(status, response_headers)    

    return [html.encode('utf-8')]

def delete_product(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        form = dict(FieldStorage(fp=environ['wsgi.input'], environ=environ))
        
        product_id = form['product_id'].value
        product_name = Product.select_one(product_id)['name']

        Product.delete(product_id)

        # alerts = [{
        #             'context': 'danger', 
        #             'message': 'Deleted {}'.format(product_name)
        #         }]


        status, response_headers = redirect('/')
        start_response(status, response_headers)    

        return ['1'.encode('utf-8')]

def edit_product(environ, start_response):
    product_id = parse_qs(environ['QUERY_STRING'])['id'][0]
    product = Product.select_one(product_id)
    html = Templite(read_html('edit_product'), {'product': product, 'alerts': None}).render()

    if environ['REQUEST_METHOD'] == 'POST':
        form = dict(FieldStorage(fp=environ['wsgi.input'], environ=environ))
        
        product_id = form['id'][0].value
        name = form['name'].value
        description = form['description'].value
        price = form['price'].value
        stock = form['stock'].value

        data = {
            'name': form['name'].value,
            'description': form['description'].value,
            'price': form['price'].value,
            'stock': form['stock'].value,
        }

        try:
            Product.update(data, product_id)
            post_html = Templite(html, {'alerts': [{'context': 'success', 'message': 'Product added.'}]}).render()
        except Exception as e:
            print(e)

        
        status, response_headers = redirect('/product?id={}'.format(product_id))
        start_response(status, response_headers)    

        return ['1'.encode('utf-8')]
        
    status, response_headers = get_response_data(html)
    start_response(status, response_headers)

    return [html.encode('utf-8')]


def not_found(environ, start_response):
    html = read_html('404')
    _, response_headers = get_response_data(html)
    start_response('404 NOT FOUND', response_headers)    

    return [html.encode('utf-8')]
