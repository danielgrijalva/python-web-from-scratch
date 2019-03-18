from cgi import parse_qs, FieldStorage
from app.template import Templite
from .abstract_view import AbstractView

class NotFound(AbstractView):
    renderer = Templite('404')

    def serve(self):
        html = self.renderer.render()
        _, response_headers = self.get_response_data(html)
        self.start_response('404 NOT FOUND', response_headers)    

        return [html.encode('utf-8')]
