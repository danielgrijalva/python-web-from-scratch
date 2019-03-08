from .utils import read_html, get_response_data
from cgi import parse_qs, escape
from .models import Model

Product = Model('crud', 'product')

def index(environ, start_response):


    html = read_html('dashboard')
    status, response_headers = get_response_data(html)
    start_response(status, response_headers)    

    return [html.encode('utf-8')]
    

def test(environ, start_response):
    html = read_html('test')
    status, response_headers = get_response_data(html)
    start_response(status, response_headers)    

    return [html.encode('utf-8')]


def add_product(environ, start_response):
    html = read_html('add_product')
    status, response_headers = get_response_data(html)
    start_response(status, response_headers)

    return [html.encode('utf-8')]

def get_product(environ, start_response):
    print(parse_qs(environ['QUERY_STRING']))
    html = read_html('product')
    status, response_headers = get_response_data(html)
    start_response(status, response_headers)    

    return [html.encode('utf-8')]

    
def not_found(environ, start_response):
    html = read_html('404')
    _, response_headers = get_response_data(html)
    start_response('404 NOT FOUND', response_headers)    

    return [html.encode('utf-8')]