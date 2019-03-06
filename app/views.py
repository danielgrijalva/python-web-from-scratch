from .utils import read_html, get_response_data

def index(environ, start_response):
    html = read_html('index')
    status, response_headers = get_response_data(html)
    start_response(status, response_headers)    

    return [html.encode('utf-8')]
    

def test(environ, start_response):
    html = read_html('test')
    status, response_headers = get_response_data(html)
    start_response(status, response_headers)    

    return [html.encode('utf-8')]

def not_found(environ, start_response):
    html = read_html('404')
    _, response_headers = get_response_data(html)
    start_response('404 NOT FOUND', response_headers)    

    return [html.encode('utf-8')]