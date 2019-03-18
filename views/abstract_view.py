from abc import ABC, abstractmethod
from app.template import Templite
from app.models import Model

class AbstractView(ABC):
    model = Model('crud', 'product')

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    @abstractmethod
    def serve(self):
        '''
            Handle the requests.
        '''
        raise NotImplementedError


    def redirect(self, route):
        '''
            Do a 302 HTTP response towards `route`.
        '''
        status = '302 Found'
        response_headers = [
            ('Location', route)
        ]

        self.start_response(status, response_headers)    

        return ['1'.encode('utf-8')]


    def get_response_data(self, response_body):
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
        