import re

def read_html(filename):
    '''
        Read an html file into a string.
    '''

    path = 'templates/{}.html'.format(filename)

    try:
        with open(path, 'r', encoding='utf-8') as file:
            html = file.read()
            return html
    except FileNotFoundError as error:
        raise error

def get_response_data(response_body):
    '''
        Return generic status and headers of a reponse. 
        This is merely a DRY function.
    '''
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]
    
    return status, response_headers

def get_route(path, urls):
    '''
        Find a a specific /path and return its callback function.
    '''
    for regex, callback in urls:
        match = re.search(regex, path)
        if match:
            return callback
    return not_found
